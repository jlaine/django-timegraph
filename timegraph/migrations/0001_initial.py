# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Graph'
        db.create_table('timegraph_graph', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lower_limit', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('upper_limit', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='LINE', max_length=255)),
            ('is_stacked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('timegraph', ['Graph'])

        # Adding M2M table for field metrics on 'Graph'
        db.create_table('timegraph_graph_metrics', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('graph', models.ForeignKey(orm['timegraph.graph'], null=False)),
            ('metric', models.ForeignKey(orm['timegraph.metric'], null=False))
        ))
        db.create_unique('timegraph_graph_metrics', ['graph_id', 'metric_id'])

        # Adding model 'Metric'
        db.create_table('timegraph_metric', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('parameter', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('type', self.gf('django.db.models.fields.CharField')(default='float', max_length=16)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
            ('rrd_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('graph_color', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
        ))
        db.send_create_signal('timegraph', ['Metric'])


    def backwards(self, orm):
        # Deleting model 'Graph'
        db.delete_table('timegraph_graph')

        # Removing M2M table for field metrics on 'Graph'
        db.delete_table('timegraph_graph_metrics')

        # Deleting model 'Metric'
        db.delete_table('timegraph_metric')


    models = {
        'timegraph.graph': {
            'Meta': {'ordering': "['slug']", 'object_name': 'Graph'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_stacked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lower_limit': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'metrics': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['timegraph.Metric']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'LINE'", 'max_length': '255'}),
            'upper_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'timegraph.metric': {
            'Meta': {'ordering': "['name']", 'object_name': 'Metric'},
            'graph_color': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'parameter': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'rrd_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'float'", 'max_length': '16'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'})
        }
    }

    complete_apps = ['timegraph']