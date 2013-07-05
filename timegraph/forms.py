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

import time
from django import forms

class GraphForm(forms.Form):
    start = forms.IntegerField(required=False, initial=-86400)
    end = forms.IntegerField(required=False, initial=-1)
    only_graph = forms.BooleanField(required=False)
    width = forms.IntegerField(required=False, initial=300)
    height = forms.IntegerField(required=False, initial=200)
    title = forms.CharField(required=False)
    watermark = forms.CharField(required=False, initial='(c) %s Wifirst' % time.strftime('%Y'))

    def clean(self):
        """
        Cleans the user's input and sets default values.
        """
        data = self.cleaned_data

        # set defaults
        for k in self.fields:
            if (data[k] is None or data[k] == '') and (self.fields[k].initial is not None):
                data[k] = self.fields[k].initial

        # check start / end
        if data['start'] >= data['end']:
            raise forms.ValidationError('start should be less than end')

        return data

    def key(self):
        """
        Returns a key to uniquely identify the form input.
        """
        return '_'.join([ str(self.cleaned_data[k]) for k in sorted(self.cleaned_data.keys()) ]).replace(' ', '_')

    def options(self):
        """
        Returns options for rrdgraph.
        """
        options = [
            '--imgformat', 'PNG',
            '--full-size-mode',
            '--width', self.cleaned_data['width'],
            '--height', self.cleaned_data['height'],
            '--start', self.cleaned_data['start'],
            '--end', self.cleaned_data['end'],
            '--watermark', self.cleaned_data['watermark'],
            '--title', self.cleaned_data['title'],
        ]
        if self.cleaned_data['only_graph']:
            options += ['--only-graph']
        return options

