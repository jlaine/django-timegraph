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

from django.test import TestCase

from timegraph.models import format_value, Graph, Metric

class TestFormat(TestCase):
    def test_format_none(self):
        self.assertEquals(format_value(None, 'b'), '')
        self.assertEquals(format_value(None, ''), '')
        self.assertEquals(format_value('', 'b'), '')
        self.assertEquals(format_value('', ''), '')

    def test_format_int(self):
        self.assertEquals(format_value(0, 'b'), '0 b')
        self.assertEquals(format_value(1, 'b'), '1 b')
        self.assertEquals(format_value(10, 'b'), '10 b')
        self.assertEquals(format_value(100, 'b'), '100 b')
        self.assertEquals(format_value(1000, 'b'), '1.0 kb')
        self.assertEquals(format_value(10000, 'b'), '10.0 kb')
        self.assertEquals(format_value(100000, 'b'), '100.0 kb')
        self.assertEquals(format_value(1000000, 'b'), '1.0 Mb')
        self.assertEquals(format_value(10000000, 'b'), '10.0 Mb')
        self.assertEquals(format_value(100000000, 'b'), '100.0 Mb')
        self.assertEquals(format_value(1000000000, 'b'), '1.0 Gb')
        self.assertEquals(format_value(10000000000, 'b'), '10.0 Gb')
        self.assertEquals(format_value(100000000000, 'b'), '100.0 Gb')
        self.assertEquals(format_value(1000000000000, 'b'), '1.0 Tb')
        self.assertEquals(format_value(10000000000000, 'b'), '10.0 Tb')
        self.assertEquals(format_value(100000000000000, 'b'), '100.0 Tb')
        self.assertEquals(format_value(1000000000000000, 'b'), '1.0 Pb')
        self.assertEquals(format_value(10000000000000000, 'b'), '10.0 Pb')
        self.assertEquals(format_value(100000000000000000, 'b'), '100.0 Pb')
        self.assertEquals(format_value(1000000000000000000, 'b'), '1000.0 Pb')

    def test_format_float(self):
        self.assertEquals(format_value(0.0, 's'), '0.0 s')
        self.assertEquals(format_value(0.00000000000000001, 's'), u'0.0 fs')
        self.assertEquals(format_value(0.0000000000000001, 's'), u'0.1 fs')
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
        self.assertEquals(format_value(1000000000000000000.0, 's'), '1000.0 Ps')

    def test_format_percent(self):
        self.assertEquals(format_value(0.0, '%'), '0.0 %')
        self.assertEquals(format_value(0.1, '%'), '0.1 %')
        self.assertEquals(format_value(1000, '%'), '1000 %')

    def test_format_string(self):
        self.assertEquals(format_value('abc', 'foo'), 'abc foo')
        self.assertEquals(format_value('0.1.0', ''), '0.1.0')

class TestMetric(TestCase):
    def test_is_summable(self):
        m = Metric(type='bool')
        self.assertEquals(m.is_summable, False)

        m = Metric(type='float', unit='s')
        self.assertEquals(m.is_summable, True)

        m = Metric(type='float', unit=u'°C')
        self.assertEquals(m.is_summable, False)

        m = Metric(type='int', unit='err')
        self.assertEquals(m.is_summable, True)

        m = Metric(type='string')
        self.assertEquals(m.is_summable, False)
