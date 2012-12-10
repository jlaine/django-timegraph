#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = 'django-timegraph',
    description = 'monitoring graphs for django',
    version = '0.1.0',
    url = 'https://github.com/jlaine/django-timegraph',
    author = u'Jeremy Lainé',
    author_email = 'jeremy.laine@m4x.org',
    packages = ['timegraph', 'timegraph.migrations', 'timegraph.templatetags'],
    package_data = {
        'timegraph': [
            'locale/fr/LC_MESSAGES/*.mo',
            'locale/fr/LC_MESSAGES/*.po',
            'static/timegraph/static/css/*.css',
            'static/timegraph/static/js/*.js',
        ],
    })
