# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table('banking_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='User Account', max_length=25)),
            ('checking_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='checking', to=orm['banking.Checking'])),
            ('saving_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Savings', to=orm['banking.Saving'])),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=10, decimal_places=2)),
            ('date_created', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('banking', ['Account'])

        # Adding model 'Checking'
        db.create_table('banking_checking', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal('banking', ['Checking'])

        # Adding model 'Saving'
        db.create_table('banking_saving', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal('banking', ['Saving'])

        # Adding model 'Payee'
        db.create_table('banking_payee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='first', max_length=15)),
            ('last_name', self.gf('django.db.models.fields.CharField')(default='last', max_length=20)),
            ('relation', self.gf('django.db.models.fields.CharField')(default='relation', max_length=20)),
        ))
        db.send_create_signal('banking', ['Payee'])

        # Adding model 'Expense'
        db.create_table('banking_expense', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=10, decimal_places=2)),
            ('reason', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('checking_expense', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('saving_expense', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('banking', ['Expense'])

        # Adding model 'Check'
        db.create_table('banking_check', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['banking.Account'])),
            ('memo', self.gf('django.db.models.fields.TextField')()),
            ('payee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['banking.Payee'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('expense', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['banking.Expense'])),
        ))
        db.send_create_signal('banking', ['Check'])

        # Adding model 'Deposit'
        db.create_table('banking_deposit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['banking.Account'])),
            ('checking_deposit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('savings_deposit', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=20, decimal_places=2)),
        ))
        db.send_create_signal('banking', ['Deposit'])


    def backwards(self, orm):
        # Deleting model 'Account'
        db.delete_table('banking_account')

        # Deleting model 'Checking'
        db.delete_table('banking_checking')

        # Deleting model 'Saving'
        db.delete_table('banking_saving')

        # Deleting model 'Payee'
        db.delete_table('banking_payee')

        # Deleting model 'Expense'
        db.delete_table('banking_expense')

        # Deleting model 'Check'
        db.delete_table('banking_check')

        # Deleting model 'Deposit'
        db.delete_table('banking_deposit')


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
        'banking.account': {
            'Meta': {'object_name': 'Account'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'checking_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'checking'", 'to': "orm['banking.Checking']"}),
            'date_created': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'User Account'", 'max_length': '25'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'saving_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Savings'", 'to': "orm['banking.Saving']"})
        },
        'banking.check': {
            'Meta': {'object_name': 'Check'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'expense': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['banking.Expense']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memo': ('django.db.models.fields.TextField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['banking.Account']"}),
            'payee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['banking.Payee']"})
        },
        'banking.checking': {
            'Meta': {'object_name': 'Checking'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'})
        },
        'banking.deposit': {
            'Meta': {'object_name': 'Deposit'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['banking.Account']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '20', 'decimal_places': '2'}),
            'checking_deposit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'savings_deposit': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'banking.expense': {
            'Meta': {'object_name': 'Expense'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'checking_expense': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'reason': ('django.db.models.fields.TextField', [], {}),
            'saving_expense': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'banking.payee': {
            'Meta': {'object_name': 'Payee'},
            'first_name': ('django.db.models.fields.CharField', [], {'default': "'first'", 'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "'last'", 'max_length': '20'}),
            'relation': ('django.db.models.fields.CharField', [], {'default': "'relation'", 'max_length': '20'})
        },
        'banking.saving': {
            'Meta': {'object_name': 'Saving'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['banking']