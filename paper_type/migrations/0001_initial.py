# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PaperType'
        db.create_table('paper_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('weight', self.gf('django.db.models.fields.IntegerField')()),
            ('paper_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paper_category.PaperCategory'])),
        ))
        db.send_create_signal(u'paper_type', ['PaperType'])


    def backwards(self, orm):
        # Deleting model 'PaperType'
        db.delete_table('paper_type')


    models = {
        u'paper_category.papercategory': {
            'Meta': {'ordering': "['-pk']", 'object_name': 'PaperCategory', 'db_table': "'paper_category'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'paper_type.papertype': {
            'Meta': {'ordering': "['-pk']", 'object_name': 'PaperType', 'db_table': "'paper_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'paper_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['paper_category.PaperCategory']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['paper_type']