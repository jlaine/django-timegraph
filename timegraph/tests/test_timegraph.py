# -*- coding: utf-8 -*-
#
# django-timegraph - monitoring graphs for django
# Copyright (c) 2011-2012, Wifirst
# Copyright (c) 2013, Jeremy Lainé
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
import shutil
import tempfile

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

import timegraph
from timegraph.models import format_value, Graph, Metric

def setup_test_environment():
    timegraph.original_rrd_root = settings.TIMEGRAPH_RRD_ROOT
    settings.TIMEGRAPH_RRD_ROOT = tempfile.mkdtemp()

def teardown_test_environment():
    shutil.rmtree(settings.TIMEGRAPH_RRD_ROOT)

    settings.TIMEGRAPH_RRD_ROOT = timegraph.original_rrd_root
    del timegraph.original_rrd_root

class TestFormat(TestCase):
    def test_format_none(self):
        self.assertEquals(format_value(None, 'b'), '')
        self.assertEquals(format_value(None, ''), '')
        self.assertEquals(format_value('', 'b'), '')
        self.assertEquals(format_value('', ''), '')
        self.assertEquals(format_value(object(), 'b'), '')
        self.assertEquals(format_value(object(), ''), '')

    def test_format_byte(self):
        self.assertEquals(format_value(0, 'b'), '0 b')
        self.assertEquals(format_value(1, 'b'), '1 b')
        self.assertEquals(format_value(1024, 'b'), '1.0 kib')
        self.assertEquals(format_value(2048, 'b'), '2.0 kib')
        self.assertEquals(format_value(1048576, 'b'), '1.0 Mib')
        self.assertEquals(format_value(1073741824, 'b'), '1.0 Gib')
        self.assertEquals(format_value(1099511627776, 'b'), '1.0 Tib')
        self.assertEquals(format_value(1125899906842624, 'b'), '1.0 Pib')
        self.assertEquals(format_value(1152921504606846976, 'b'), '1.0 Eib')
        # FIXME: there seems to be a rounding error
        #self.assertEquals(format_value(1180591620717411303424, 'b'), '1.0 Zib')
        #self.assertEquals(format_value(1208925819614629174706176, 'b'), '1.0 Yib')
        self.assertEquals(format_value(1237940039285380274899124224, 'b'), '1024.0 Yib')

    def test_format_int(self):
        self.assertEquals(format_value(0, 's'), '0 s')
        self.assertEquals(format_value(1, 's'), '1 s')
        self.assertEquals(format_value(10, 's'), '10 s')
        self.assertEquals(format_value(100, 's'), '100 s')
        self.assertEquals(format_value(1000, 's'), '1.0 ks')
        self.assertEquals(format_value(10000, 's'), '10.0 ks')
        self.assertEquals(format_value(100000, 's'), '100.0 ks')
        self.assertEquals(format_value(1000000, 's'), '1.0 Ms')
        self.assertEquals(format_value(10000000, 's'), '10.0 Ms')
        self.assertEquals(format_value(100000000, 's'), '100.0 Ms')
        self.assertEquals(format_value(1000000000, 's'), '1.0 Gs')
        self.assertEquals(format_value(10000000000, 's'), '10.0 Gs')
        self.assertEquals(format_value(100000000000, 's'), '100.0 Gs')
        self.assertEquals(format_value(1000000000000, 's'), '1.0 Ts')
        self.assertEquals(format_value(10000000000000, 's'), '10.0 Ts')
        self.assertEquals(format_value(100000000000000, 's'), '100.0 Ts')
        self.assertEquals(format_value(1000000000000000, 's'), '1.0 Ps')
        self.assertEquals(format_value(10000000000000000, 's'), '10.0 Ps')
        self.assertEquals(format_value(100000000000000000, 's'), '100.0 Ps')
        self.assertEquals(format_value(1000000000000000000, 's'), '1.0 Es')
        self.assertEquals(format_value(10000000000000000000, 's'), '10.0 Es')
        self.assertEquals(format_value(100000000000000000000, 's'), '100.0 Es')
        self.assertEquals(format_value(1000000000000000000000, 's'), '1.0 Zs')
        self.assertEquals(format_value(10000000000000000000000, 's'), '10.0 Zs')
        self.assertEquals(format_value(1000000000000000000000000, 's'), '1.0 Ys')
        self.assertEquals(format_value(10000000000000000000000000, 's'), '10.0 Ys')
        self.assertEquals(format_value(100000000000000000000000000, 's'), '100.0 Ys')
        self.assertEquals(format_value(1000000000000000000000000000, 's'), '1000.0 Ys')
        self.assertEquals(format_value(10000000000000000000000000000, 's'), '10000.0 Ys')

    def test_format_float(self):
        self.assertEquals(format_value(0.0, 's'), '0.0 s')
        self.assertEquals(format_value(0.00000000000000000000000001, 's'), u'0.0 ys')
        self.assertEquals(format_value(0.0000000000000000000000001, 's'), u'0.1 ys')
        self.assertEquals(format_value(0.000000000000000000000001, 's'), u'1.0 ys')
        self.assertEquals(format_value(0.00000000000000000000001, 's'), u'10.0 ys')
        self.assertEquals(format_value(0.0000000000000000000001, 's'), u'100.0 ys')
        self.assertEquals(format_value(0.000000000000000000001, 's'), u'1.0 zs')
        self.assertEquals(format_value(0.00000000000000000001, 's'), u'10.0 zs')
        self.assertEquals(format_value(0.0000000000000000001, 's'), u'100.0 zs')
        self.assertEquals(format_value(0.000000000000000001, 's'), u'1.0 as')
        self.assertEquals(format_value(0.00000000000000001, 's'), u'10.0 as')
        self.assertEquals(format_value(0.0000000000000001, 's'), u'100.0 as')
        self.assertEquals(format_value(0.000000000000001, 's'), u'1.0 fs')
        self.assertEquals(format_value(0.00000000000001, 's'), u'10.0 fs')
        self.assertEquals(format_value(0.0000000000001, 's'), u'100.0 fs')
        self.assertEquals(format_value(0.000000000001, 's'), u'1.0 ps')
        self.assertEquals(format_value(0.00000000001, 's'), u'10.0 ps')
        self.assertEquals(format_value(0.0000000001, 's'), u'100.0 ps')
        self.assertEquals(format_value(0.000000001, 's'), u'1.0 ns')
        self.assertEquals(format_value(0.00000001, 's'), u'10.0 ns')
        self.assertEquals(format_value(0.0000001, 's'), u'100.0 ns')
        self.assertEquals(format_value(0.000001, 's'), u'1.0 µs')
        self.assertEquals(format_value(0.00001, 's'), u'10.0 µs')
        self.assertEquals(format_value(0.0001, 's'), u'100.0 µs')
        self.assertEquals(format_value(0.001, 's'), '1.0 ms')
        self.assertEquals(format_value(0.01, 's'), '10.0 ms')
        self.assertEquals(format_value(0.1, 's'), '100.0 ms')
        self.assertEquals(format_value(1.0, 's'), '1.0 s')
        self.assertEquals(format_value(10.0, 's'), '10.0 s')
        self.assertEquals(format_value(100.0, 's'), '100.0 s')
        self.assertEquals(format_value(1000.0, 's'), '1.0 ks')
        self.assertEquals(format_value(10000.0, 's'), '10.0 ks')
        self.assertEquals(format_value(100000.0, 's'), '100.0 ks')
        self.assertEquals(format_value(1000000.0, 's'), '1.0 Ms')
        self.assertEquals(format_value(10000000.0, 's'), '10.0 Ms')
        self.assertEquals(format_value(100000000.0, 's'), '100.0 Ms')
        self.assertEquals(format_value(1000000000.0, 's'), '1.0 Gs')
        self.assertEquals(format_value(10000000000.0, 's'), '10.0 Gs')
        self.assertEquals(format_value(100000000000.0, 's'), '100.0 Gs')
        self.assertEquals(format_value(1000000000000.0, 's'), '1.0 Ts')
        self.assertEquals(format_value(10000000000000.0, 's'), '10.0 Ts')
        self.assertEquals(format_value(100000000000000.0, 's'), '100.0 Ts')
        self.assertEquals(format_value(1000000000000000.0, 's'), '1.0 Ps')
        self.assertEquals(format_value(10000000000000000.0, 's'), '10.0 Ps')
        self.assertEquals(format_value(100000000000000000.0, 's'), '100.0 Ps')
        self.assertEquals(format_value(1000000000000000000.0, 's'), '1.0 Es')
        self.assertEquals(format_value(10000000000000000000.0, 's'), '10.0 Es')
        self.assertEquals(format_value(100000000000000000000.0, 's'), '100.0 Es')
        self.assertEquals(format_value(1000000000000000000000.0, 's'), '1.0 Zs')
        self.assertEquals(format_value(10000000000000000000000.0, 's'), '10.0 Zs')
        self.assertEquals(format_value(100000000000000000000000.0, 's'), '100.0 Zs')
        self.assertEquals(format_value(1000000000000000000000000.0, 's'), '1.0 Ys')
        self.assertEquals(format_value(10000000000000000000000000.0, 's'), '10.0 Ys')
        self.assertEquals(format_value(100000000000000000000000000.0, 's'), '100.0 Ys')
        self.assertEquals(format_value(1000000000000000000000000000.0, 's'), '1000.0 Ys')
        self.assertEquals(format_value(10000000000000000000000000000.0, 's'), '10000.0 Ys')

    def test_format_percent(self):
        self.assertEquals(format_value(0.0, '%'), '0.0 %')
        self.assertEquals(format_value(0.1, '%'), '0.1 %')
        self.assertEquals(format_value(1000, '%'), '1000 %')

    def test_format_string(self):
        self.assertEquals(format_value('abc', 'foo'), 'abc foo')
        self.assertEquals(format_value('0.1.0', ''), '0.1.0')

class TestGraph(TestCase):
    def test_unicode(self):
        m = Graph(title='foo bar')
        self.assertEquals(unicode(m), 'foo bar')

class TestMetric(TestCase):
    fixtures = ['test_timegraph_metrics.json', 'test_timegraph_users.json']

    def setUp(self):
        setup_test_environment()

    def tearDown(self):
        teardown_test_environment()

    def test_is_summable(self):
        m = Metric(type='bool')
        self.assertEquals(m.is_summable, False)

        m = Metric(type='float', unit='s')
        self.assertEquals(m.is_summable, True)

        m = Metric(type='float', unit=u'°C')
        self.assertEquals(m.is_summable, False)

        m = Metric(type='float', unit=u'°F')
        self.assertEquals(m.is_summable, False)

        m = Metric(type='int', unit='err')
        self.assertEquals(m.is_summable, True)

        m = Metric(type='int', unit='%')
        self.assertEquals(m.is_summable, False)

        m = Metric(type='string')
        self.assertEquals(m.is_summable, False)

    def test_set_get(self):
        metric = Metric.objects.get(pk=1)
        user = User.objects.get(pk=1)
        metric.set_polling(user, '1.23')

        value = metric.get_polling(user)
        self.assertEquals(value, 1.23)

    def test_to_python_bool(self):
        m = Metric(type='bool')
        self.assertEquals(m.to_python(None), False)
        self.assertEquals(m.to_python(''), False)
        self.assertEquals(m.to_python('0'), False)
        self.assertEquals(m.to_python('False'), False)
        self.assertEquals(m.to_python('True'), True)
        self.assertEquals(m.to_python('1'), True)

    def test_to_python_float(self):
        m = Metric(type='float')
        self.assertEquals(m.to_python(None), 0.0)
        self.assertEquals(m.to_python(''), 0.0)
        self.assertEquals(m.to_python('0.0'), 0.0)
        self.assertEquals(m.to_python('1.3'), 1.3)
        self.assertEquals(m.to_python('10.1'), 10.1)

    def test_to_python_int(self):
        m = Metric(type='int')
        self.assertEquals(m.to_python(None), 0)
        self.assertEquals(m.to_python(''), 0)
        self.assertEquals(m.to_python('0'), 0)
        self.assertEquals(m.to_python('1'), 1)
        self.assertEquals(m.to_python('10'), 10)

    def test_to_python_string(self):
        m = Metric(type='string')
        self.assertEquals(m.to_python(None), '')
        self.assertEquals(m.to_python(''), '')
        self.assertEquals(m.to_python('0'), '0')
        self.assertEquals(m.to_python('1'), '1')
        self.assertEquals(m.to_python('abcd'), 'abcd')

    def test_pre_key(self):
        metric = Metric.objects.get(pk=1)
        user = User.objects.get(pk=1)
        self.assertEquals(metric._pre_key_for(user) % user.pk, '%s/user/1/1' % settings.TIMEGRAPH_CACHE_PREFIX)

    def test_rrd_path(self):
        metric = Metric.objects.get(pk=1)
        user = User.objects.get(pk=1)
        self.assertEquals(metric._rrd_path(user), os.path.join(settings.TIMEGRAPH_RRD_ROOT, 'user', '1', '1.rrd'))

    def test_unicode(self):
        m = Metric(name='foo bar')
        self.assertEquals(unicode(m), 'foo bar')
