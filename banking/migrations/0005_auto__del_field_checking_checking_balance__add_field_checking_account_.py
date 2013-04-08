# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Checking.checking_balance'
        db.delete_column('banking_checking', 'checking_balance')

        # Adding field 'Checking.account'
        db.add_column('banking_checking', 'account',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['banking.Account']),
                      keep_default=False)

        # Adding field 'Account.checking_account'
        db.add_column('banking_account', 'checking_account',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='checking', to=orm['banking.Checking']),
                      keep_default=False)

        # Adding field 'Account.saving_account'
        db.add_column('banking_account', 'saving_account',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='Savings', to=orm['banking.Saving']),
                      keep_default=False)

        # Deleting field 'Saving.saving_balance'
        db.delete_column('banking_saving', 'saving_balance')

        # Adding field 'Saving.account'
        db.add_column('banking_saving', 'account',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['banking.Account']),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Checking.checking_balance'
        raise RuntimeError("Cannot reverse this migration. 'Checking.checking_balance' and its values cannot be restored.")
        # Deleting field 'Checking.account'
        db.delete_column('banking_checking', 'account_id')

        # Deleting field 'Account.checking_account'
        db.delete_column('banking_account', 'checking_account_id')

        # Deleting field 'Account.saving_account'
        db.delete_column('banking_account', 'saving_account_id')


        # User chose to not deal with backwards NULL issues for 'Saving.saving_balance'
        raise RuntimeError("Cannot reverse this migration. 'Saving.saving_balance' and its values cannot be restored.")
        # Deleting field 'Saving.account'
        db.delete_column('banking_saving', 'account_id')


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
            'account_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'checking_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'checking'", 'to': "orm['banking.Checking']"}),
            'date_created': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'User Account'", 'max_length': '25'}),
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
            'account': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': "orm['banking.Account']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'banking.expense': {
            'Meta': {'object_name': 'Expense'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'checking_expense': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['banking.Account']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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