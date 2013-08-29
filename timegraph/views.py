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
import rrdtool
import tempfile

from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.utils.encoding import force_unicode

from timegraph.forms import GraphForm
from timegraph.models import format_value

# colors from munin
COLORS = [
    '#00CC00', '#0066B3', '#FF8000', '#FFCC00', '#330099', '#990099', '#CCFF00', '#FF0000', '#808080',
    '#008F00', '#00487D', '#B35A00', '#B38F00', '#6B006B', '#8FB300', '#B30000', '#BEBEBE',
    '#80FF80', '#80C9FF', '#FFC080', '#FFE680', '#AA80FF', '#EE00CC', '#FF8080',
    '#666600', '#FFBFFF', '#00FFCC', '#CC6699', '#999900',
]

def render_graph(request, graph, obj):
    """
    Renders the specified graph.
    """
    # validate input
    form = GraphForm(request.GET)
    if not form.is_valid():
        return HttpResponseBadRequest()

    count = 0
    options = []
    if graph.is_stacked:
        stack = ':STACK'
    else:
        stack = ''
    is_memory = False
    for metric in graph.metrics.order_by('graph_order'):
        if metric.unit in ['b', 'B']:
            is_memory = True
        data_file = metric._rrd_path(obj)
        value = metric.get_polling(obj)
        if os.path.exists(data_file):
            color = metric.graph_color
            if not color:
                color = COLORS[count % len(COLORS)]

            # current value
            value_str = format_value(value, metric.unit)
            if value_str:
                value_str = ' | ' + value_str

            options += [
                'DEF:%s=%s:%s:AVERAGE' % (count, data_file, metric.pk),
                '%s:%s%s:%s%s%s' % (graph.type, count, color, metric.name, value_str, stack)]
            count += 1

    # if no RRDs were found stop here
    if not count:
        raise Http404

    if is_memory:
        options += ['--base', '1024']
    if graph.lower_limit is not None:
        options += [ '--lower-limit', str(graph.lower_limit) ]
        options += [ '-r' ]
    if graph.upper_limit is not None:
        options += [ '--upper-limit', str(graph.upper_limit) ]
    options += form.options()
    image_data = timegraph_rrd(options)

    return HttpResponse(image_data, mimetype='image/png')

def render_metric(request, metric, object_list):
    """
    Renders the total for the given metric.
    """
    # validate input
    form = GraphForm(request.GET)
    if not form.is_valid():
        return HttpResponseBadRequest()

    color = metric.graph_color
    if not color:
        color = '#990033'

    count = 0
    options = []
    type = 'AREA'
    for obj in object_list:
        data_file = metric._rrd_path(obj)
        if os.path.exists(data_file):
            options += [
                'DEF:%s=%s:%s:AVERAGE' % (count, data_file, metric.pk),
                '%s:%s%s' % (type, count, color)]
            type = 'STACK'
            count += 1

    # if no RRDs were found stop here
    if not count:
        raise Http404

    options += form.options()
    image_data = timegraph_rrd(options)

    return HttpResponse(image_data, mimetype='image/png')

def timegraph_rrd(options):
    """
    Invokes rrd_graph with the given options and returns the image data.
    """
    image_file = tempfile.NamedTemporaryFile()
    rrdtool.graph([str(image_file.name)] + [ force_unicode(x).encode('utf-8') for x in options ])
    return image_file.read()
