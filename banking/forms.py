__author__ = 'Brandon'
#System Imports
import datetime
from banking.models import *
#Django Imports
from django import forms
from banking.models import Payee,Check
from django.contrib.auth.forms import *


class CheckForm(forms.ModelForm):
    class Meta:
        model = Check


class ExpenseForm(forms.ModelForm):
        class Meta:
            model = Expense


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit


#Works
class PayeeForm(forms.ModelForm):
    class Meta:
        model = Payee


class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Withdraw


#Don't worry about this for now.
class AuthForm(AuthenticationForm):
    pass


#Dont worry about this for now, only needs to work for me.
class AccountForm(forms.ModelForm):
    user_name = forms.CharField(max_length=25)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input_text'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input_text'}), label='Retype Password')

    class Meta:
        model = Account
        exclude = ('owner', 'saving_account', 'checking_account','balance','date_created',)

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(AccountForm, self).save(commit=False)
        user = User.objects.create_user(username=m.first_name, email=m.email, password=m.password1)
        if commit:
            m.save()
        return m

