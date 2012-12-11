# -*- coding: utf-8 -*-
#
# django-timegraph - monitoring graphs for django
# Copyright (c) 2011-2012, Wifirst
# All rights reserved.
#
# See AUTHORS file for a full list of contributors.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright notice, 
#        this list of conditions and the following disclaimer.
#     
#     2. Redistributions in binary form must reproduce the above copyright 
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
#     3. Neither the name of Wifirst nor the names of its contributors
#        may be used to endorse or promote products derived from this software
#        without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import os
import rrdtool
import time

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Graph(models.Model):
    """
    A model representing a graph of a set of monitored metrics.
    """
    slug = models.SlugField()
    metrics = models.ManyToManyField('Metric')
    title = models.CharField(max_length=255)
    lower_limit = models.IntegerField(blank=True, null=True, default=0)
    upper_limit = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=255, default='LINE')
    is_stacked = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['slug']
        verbose_name = _('graph')
        verbose_name_plural = _('graphs')

class Metric(models.Model):
    """
    A model representing a monitored metric.
    """

    TYPE_CHOICES = (
        ('bool', 'boolean'),
        ('float', 'float'),
        ('int', 'integer'),
        ('str', 'string'),
    )

    name = models.CharField(max_length=32, verbose_name=_('name'))
    parameter = models.CharField(max_length=256, verbose_name=_('parameter'))
    type = models.CharField(max_length=16, choices=TYPE_CHOICES, default='float')
    unit = models.CharField(max_length=6, blank=True, verbose_name=_('unit'))
    rrd_enabled = models.BooleanField(default=True, verbose_name=_('RRD enabled'))
    graph_color = models.CharField(blank=True, max_length=8, verbose_name=_('graph color'))

    def get_polling(self, obj):
        """
        Retrieves the latest value of the metric the given object.
        """
        return self.to_python(cache.get(self.__cache_key(obj)))

    def set_polling(self, obj, value):
        """
        Stores the latest value of the metric for the given object.
        """
        cache.set(self.__cache_key(obj), value, 7 * 86400)
        if self.rrd_enabled:
            filepath = self.rrd_path(obj)
            if not os.path.exists(filepath):
                dirpath = os.path.dirname(filepath)
                if not os.path.exists(dirpath):
                    os.makedirs(dirpath)
                rrdtool.create(filepath , 'DS:%s:GAUGE:300:U:U' % self.id,
                    'RRA:AVERAGE:0.5:1:600',
                    'RRA:AVERAGE:0.5:6:600',
                    'RRA:AVERAGE:0.5:24:600',
                    'RRA:AVERAGE:0.5:288:600',
                    'RRA:MAX:0.5:1:600',
                    'RRA:MAX:0.5:6:600',
                    'RRA:MAX:0.5:24:600',
                    'RRA:MAX:0.5:288:600') # Up to 600d
            rrdtool.update(filepath, str("%i:%s" % (int(time.time()), value)))

    @property
    def is_summable(self):
        """
        True if the metric is summable, False otherwise.
        """
        return (self.type in ['float', 'int']) and (self.unit not in [u'%', u'°', u'°C', u'°F'])

    def to_python(self, value):
        """
        Converts the given string value to a python value.
        """
        if self.type == 'float':
            return value and float(value) or 0.0
        elif self.type == 'int':
            return value and int(value) or 0
        elif self.type == 'bool':
            return value in ['1', 'True']
        return value

    def rrd_path(self, obj):
        """
        RRD path for the given object.
        """
        obj_type = obj.__class__.__name__.lower()
        obj_pk = str(obj.pk).replace(':', '')
        return os.path.join(settings.TIMEGRAPH_RRD_ROOT, obj_type, obj_pk, '%s.rrd' % self.pk)

    def __cache_key(self, obj):
        """
        Cache key for the given object.
        """
        obj_type = obj.__class__.__name__.lower()
        obj_pk = str(obj.pk).replace(':', '')
        return '%s/%s/%s/%s' % (settings.TIMEGRAPH_CACHE_ROOT, obj_type, obj_pk, self.pk)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('metric')
        verbose_name_plural = _('metrics')

def format_with_prefix(value, unit):
    """
    Formats a float value with the appropriate SI prefix.
    """
    if value >= 1000000000000000:
        return u'%.1f P%s' % (value / 1000000000000000.0, unit)
    elif value >= 1000000000000:
        return u'%.1f T%s' % (value / 1000000000000.0, unit)
    elif value >= 1000000000:
        return u'%.1f G%s' % (value / 1000000000.0, unit)
    elif value >= 1000000:
        return u'%.1f M%s' % (value / 1000000.0, unit)
    elif value >= 1000:
        return u'%.1f k%s' % (value / 1000.0, unit)
    elif value >= 1 or not value:
        return u'%.1f %s' % (value, unit)
    elif value >= 0.001:
        return u'%.1f m%s' % (value * 1000.0, unit)
    elif value >= 0.000001:
        return u'%.1f µ%s' % (value * 1000000.0, unit)
    elif value >= 0.000000001:
        return u'%.1f n%s' % (value * 1000000000.0, unit)
    elif value >= 0.000000000001:
        return u'%.1f p%s' % (value * 1000000000000.0, unit)
    else:
        return u'%.1f f%s' % (value * 1000000000000000.0, unit)
    
def format_value(value, unit):
    """
    Formats the given value with the specified unit.
    """
    if value in [None, '']:
        return ''

    if isinstance(value, bool) or isinstance(value, str) or isinstance(value, unicode):
        if unit:
            return '%s %s' % (value, unit)
        else:
            return value

    if isinstance(value, float):
        if unit in [u'%', u'°', u'°C', u'°F']:
            return '%.1f %s' % (value, unit)
        else:
            return format_with_prefix(value, unit)

    if isinstance(value, int) or isinstance(value, long):
        if unit in [u'%', u'°', u'°C', u'°F'] or value < 1000:
            return '%i %s' % (value, unit)
        else:
            return format_with_prefix(value, unit)

    return ''
