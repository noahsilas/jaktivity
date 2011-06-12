# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Log'
        db.create_table('jaktivity_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('view', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('response_status', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('exception_type', self.gf('django.db.models.fields.CharField')(max_length=256, null=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
        ))
        db.send_create_signal('jaktivity', ['Log'])

        # Adding model 'HTTPHeader'
        db.create_table('jaktivity_httpheader', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('log', self.gf('django.db.models.fields.related.ForeignKey')(related_name='headers', to=orm['jaktivity.Log'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('value', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('jaktivity', ['HTTPHeader'])

        # Adding model 'HTTPParam'
        db.create_table('jaktivity_httpparam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('log', self.gf('django.db.models.fields.related.ForeignKey')(related_name='http_params', to=orm['jaktivity.Log'])),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('value', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('jaktivity', ['HTTPParam'])

        # Adding model 'ViewParam'
        db.create_table('jaktivity_viewparam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('log', self.gf('django.db.models.fields.related.ForeignKey')(related_name='view_params', to=orm['jaktivity.Log'])),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True)),
            ('value', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('jaktivity', ['ViewParam'])

        # Adding model 'Note'
        db.create_table('jaktivity_note', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('log', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notes', to=orm['jaktivity.Log'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('jaktivity', ['Note'])


    def backwards(self, orm):
        
        # Deleting model 'Log'
        db.delete_table('jaktivity_log')

        # Deleting model 'HTTPHeader'
        db.delete_table('jaktivity_httpheader')

        # Deleting model 'HTTPParam'
        db.delete_table('jaktivity_httpparam')

        # Deleting model 'ViewParam'
        db.delete_table('jaktivity_viewparam')

        # Deleting model 'Note'
        db.delete_table('jaktivity_note')


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
