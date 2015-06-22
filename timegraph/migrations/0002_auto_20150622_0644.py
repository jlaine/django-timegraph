# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timegraph', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graph',
            name='type',
            field=models.CharField(default=b'LINE', max_length=255, choices=[(b'AREA', b'area'), (b'LINE', b'line')]),
            preserve_default=True,
        ),
    ]
