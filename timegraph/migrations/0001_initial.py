# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
                ('title', models.CharField(max_length=255)),
                ('lower_limit', models.IntegerField(default=0, null=True, blank=True)),
                ('upper_limit', models.IntegerField(null=True, blank=True)),
                ('type', models.CharField(default=b'LINE', max_length=255)),
                ('is_stacked', models.BooleanField(default=False)),
                ('is_visible', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['slug'],
                'verbose_name': 'graph',
                'verbose_name_plural': 'graphs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='name')),
                ('parameter', models.CharField(max_length=256, verbose_name='parameter')),
                ('type', models.CharField(default=b'float', max_length=16, choices=[(b'bool', b'boolean'), (b'float', b'float'), (b'int', b'integer'), (b'str', b'string')])),
                ('unit', models.CharField(max_length=6, verbose_name='unit', blank=True)),
                ('rrd_enabled', models.BooleanField(default=True, verbose_name='RRD enabled')),
                ('graph_color', models.CharField(max_length=8, verbose_name='graph color', blank=True)),
                ('graph_order', models.IntegerField(default=0, verbose_name='graph order')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'metric',
                'verbose_name_plural': 'metrics',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='graph',
            name='metrics',
            field=models.ManyToManyField(to='timegraph.Metric'),
            preserve_default=True,
        ),
    ]
