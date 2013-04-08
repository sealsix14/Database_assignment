__author__ = 'Brandon'
#System Imports
import datetime
from banking.models import *
#Django Imports
from django import forms
from banking.models import Payee,Check


class CheckForm(forms.Form):
    class Meta:
        model = Check


class ExpenseForm(forms.ModelForm):
        class Meta:
            model = Expense

class DepositForm(forms.ModelForm):

    class Meta:
        model = Deposit