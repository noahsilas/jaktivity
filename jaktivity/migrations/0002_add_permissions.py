# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from django.db.models import get_app 
from django.contrib.auth.management import create_permissions 

class Migration(DataMigration):

    def forwards(self, orm):
        """ Adds custom model permissions to the DB"""
        # south doesn't support custom permissions very well.
        # this should get updated when south ticket #211 is
        # closed. http://south.aeracode.org/ticket/211
        create_permissions(get_app("jaktivity"), (), 0)

    def backwards(self, orm):
        """ No-op.
            Django permissions are a touch fidgety, since they are keyed
            non-deterministically. You will have to manually remove the
            permission.
        """

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'jaktivity.httpheader': {
            'Meta': {'object_name': 'HTTPHeader'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'headers'", 'to': "orm['jaktivity.Log']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'jaktivity.httpparam': {
            'Meta': {'object_name': 'HTTPParam'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'http_params'", 'to': "orm['jaktivity.Log']"}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'jaktivity.log': {
            'Meta': {'object_name': 'Log'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'exception_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'response_status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'view': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'jaktivity.note': {
            'Meta': {'object_name': 'Note'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notes'", 'to': "orm['jaktivity.Log']"})
        },
        'jaktivity.viewparam': {
            'Meta': {'object_name': 'ViewParam'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'view_params'", 'to': "orm['jaktivity.Log']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True'})
        }
    }

    complete_apps = ['jaktivity']
