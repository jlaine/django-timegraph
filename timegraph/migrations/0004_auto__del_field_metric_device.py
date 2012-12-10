# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Metric.device'
        db.delete_column('timegraph_metric', 'device')


    def backwards(self, orm):
        
        # Adding field 'Metric.device'
        db.add_column('timegraph_metric', 'device', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    models = {
        'timegraph.graph': {
            'Meta': {'ordering': "['slug']", 'object_name': 'Graph'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_stacked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lower_limit': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'metrics': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['timegraph.Metric']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
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
