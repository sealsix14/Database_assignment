"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from banking.models import *
import datetime
class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class CheckTest(TestCase):

    def createCheck(self):
        """
        Test to create a check and save it in the system
        we need to ensure that we can add a check and correctly
        update the databases' overall account balance.
        """
        user = User.objects.get(first_name='brandon')
        check = Check()
        check.expense = Expense()
        check.expense.saving_expense = True
        check.expense.checking_expense = False
        check.expense.amount = 350
        check.expense.date = datetime.date
        check.expense.owner = user
        check.expense.reason = 'RENT'
        check.date = datetime.date
        check.memo = 'needed to pay rent'
        check.payee = Payee()
        check.payee.first_name = 'reese'
        check.payee.last_name = 'jacobs'
        check.payee.relation = 'family'
        check.check_number = check.number
        check.save()
        self.assertTrue(check.validate_unique())



