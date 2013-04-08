from django.db import models
from django.contrib.auth.models import User
import datetime

#Main model that does the work in the views


class Account(models.Model):

    #Gets account, calls self.objects.get() but encapsulates it into a method
    def get_account(self,Owner):
        ow = self.objects.get(owner=Owner)
        return ow

    #Grabs the balance and returns it
    def get_balance(self):
        return self.balance

    def get_balance_by_user(self,Owner):
        account = self.objects.get(owner=Owner)
        return account.balance

    #Updates total amount of money in Savings and Checking Accounts
    def update_balance(self):
        self.balance += self.checking_account.balance
        self.balance += self.saving_account.saving_balance

    #Return the total amount of money that has been written via checks, access the expense of each check
    def get_check_total(self):
        check_total = 0
        total_checks = Check.objects.filter(owner=self)
        for check in total_checks:
            check_total += check.expense.amount

    def get_deposit_total(self):
        deposit_total = 0
        total_deposits = Deposit.objects.filter(account=self)
        for deposit in total_deposits:
            deposit_total += deposit.amount
        return deposit_total

    def get_withdraw_total(self):
        total = 0
        withdraws=Withdraw.objects.filter(account=self)
        for withdraw in withdraws:
            total += withdraw.amount
        return total

    def get_savings_balance(self):
        return self.saving_account.balance

    def get_checking_balance(self):
        return self.checking_account.balance

    def get_balance(self, Savings =False, Checking=False):
        if Savings:
            return self.get_savings_balance
        if Checking:
            return self.get_checking_balance
        else:
            total = self.checking_account.balance + self.saving_account.balance
            return  total

    def get_checking_account(self):
        return self.checking_account

    def get_savings_account(self):
        return self.saving_account

    #Fields for the Table
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=25,default="User Account")
    checking_account = models.ForeignKey('Checking', related_name="checking")
    saving_account = models.ForeignKey('Saving', related_name="Savings")
    balance = models.DecimalField(verbose_name="Account Balance",decimal_places=2, max_digits=10, default=0.0)
    date_created = models.DateField()

    def __unicode__(self):
        return self.name


class Checking(models.Model):
    #Methods for Values in model

    def checks_Written(self):
        checks = Check.objects.count()
        return checks

    def get_checks_by_owner(self,Owner):
        account_owner = Account.objects.get(owner=Owner)
        checks = Check.objects.filter(owner=account_owner)

    def get_balance(self,Owner):
        this_account = Account.objects.get(owner=Owner)
        checks = Check.objects.all()
        deposits = Deposit.objects.all()
        checks = checks.filter(owner=this_account)
        deposits = deposits.filter(account=this_account)
        #Filter checks and deposits by Account
        balance = 0
        for check in checks:
            if check.expense.amount > 0:
                balance -= check.expense.amount
        for deposit in deposits:
            if deposit.checking_deposit:
                balance += deposit.amount


    name = models.CharField(max_length=25,default="Users Checking")
    owner = models.ForeignKey(User,blank=False, null=True, on_delete=models.SET_NULL)
    balance = models.DecimalField(verbose_name="Checking Balance",decimal_places=2,max_digits=10,default=0.0)
    owners_account = models.ForeignKey(Account)

    def __unicode__(self):
        return self.name


class Saving(models.Model):

    def get_balance(self):
        expenses = Expense.objects
        balance = 0
        expenses = Expense.objects.filter(saving_expense=True)
        for expense in expenses:
            balance += expense.amount
        return balance

    owner = models.ForeignKey(User,blank=False, null=True, on_delete=models.SET_NULL)
    balance = models.DecimalField(verbose_name="Saving Balance",decimal_places=2, max_digits=10, default=0.0)
    owners_account = models.ForeignKey(Account)
    saving_balance = get_balance
    name = models.CharField(max_length=25,default="Users Savings")

    def __unicode__(self):
        return self.name


class Payee(models.Model):
    first_name = models.CharField(max_length=15, default='first')
    last_name = models.CharField(max_length=20, default='last')
    relation = models.CharField(max_length=20, default='relation')

    def __unicode__(self):
        return self.last_name


#Create Expenses that can be used for the amount on checks
class Expense(models.Model):

    def get_expenses_by_user(self,Owner):
        account_owner = Account.objects.get(owner=Owner)
        expenses = Expense.objects.filter(owner=account_owner.owner)
        return expenses

    def get_expenses_by_account(self, Owner, Checking=False, Saving=False):
        expenses = self.get_expenses_by_user(Owner)
        if Checking:
            expenses.filter(checking_expense=True)
        if Saving:
            expenses.filter(saving_expense=True)
        return expenses

    owner = models.ForeignKey(User,blank=False,null=True,on_delete=models.SET_NULL)
    amount = models.DecimalField(verbose_name="Expense Amount", decimal_places=2,max_digits=10, default=0.0)
    reason = models.TextField()
    date = models.DateField()
    checking_expense = models.BooleanField(default=True)
    saving_expense = models.BooleanField(default=False)

    def __unicode__(self):
        return self.reason

#Checks owner is an Account, as compared to Accounts owner which is a User.
class Check(models.Model):

    def number(self):
        no = self.objects.count()
        if no is None:
            return 1
        else:
            return no + 1

    def get_total_deficit(self):
        total = 0
        checks = Check.objects.all()
        for check in checks:
            total -= check.expense.amount
        return total

    owner = models.ForeignKey(Account)
    memo = models.TextField()
    payee = models.ForeignKey(Payee)
    date = models.DateTimeField()
    expense = models.ForeignKey(Expense)
    check_number = models.IntegerField(max_length=200, default=number)

    def __unicode__(self):
        return str(self.check_number)


class Deposit(models.Model):
    account = models.ForeignKey('Account')
    checking_deposit = models.BooleanField(default=False)
    savings_deposit = models.BooleanField(default=True)
    amount = models.DecimalField(verbose_name="Deposit Amount", decimal_places=2, max_digits=20,default=0.0)

    def get_total_income(self):
        total=0
        deposits = Deposit.objects.all()
        for deposit in deposits:
            total += deposit.amount
        return total

class Withdraw(models.Model):
    account = models.ForeignKey('Account')
    amount = models.DecimalField(verbose_name="Expense Amount", decimal_places=2,max_digits=10, default=0.0)
    date = models.DateTimeField()
    location = models.TextField(max_length=300,default="LOCATION OF WITHDRAW")

    def get_withdraws(self, Owner=False):
        if Owner:
            a = Account.objects.get(owner=Owner)
            withdrawls = Withdraw.objects.filter(account=a)
        else:
            withdrawls = Withdraw.objects.all()
        return withdrawls


    def get_withdraw_amount(self,Owner):
        total = 0
        a = Account.objects.get(owner=Owner)
        withdraws = Withdraw.objects.filter(account=a)
        for withdraw in withdraws:
            total += withdraw.amount
        return total

