from django.db import models
from django.contrib.auth.models import User
import datetime


class Account(models.Model):

    #Fields for the Table
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    account_name = models.CharField(max_length=25,default="User Account")
    checking_account = models.ForeignKey('Checking', related_name="checking")
    saving_account = models.ForeignKey('Saving', related_name="Savings")
    #Hide balance field in the admin panel.
    balance = models.DecimalField(verbose_name="Account Balance",decimal_places=2, max_digits=10, default=0.0)
    #saving_balance = saving_account.balance
    #checking_balance = checking_account.balance
    date_created = models.DateField(auto_now_add=True)

    #Gets account, calls self.objects.get() but encapsulates it into a method
    def get_account_by_owner(self, Owner):
        ow = self.objects.get(owner=Owner)
        return ow

    #Get the aggregate of the deposit amounts, withdraw amounts, and check amounts to sum a total.
    def get_balance(self):
        deposits = Deposit.objects.filter(owner=self)
        withdraws = Withdraw.objects.filter(owner=self)
        checks = Check.objects.filter(owner=self)
        deposits = deposits.aggregate(sum('amount'))
        withdraws = withdraws.aggregate(sum('amount'))
        checks = checks.aggregate(sum('amount'))
        #Total up the deposit sum, withdraw sum, and check sum into a total.
        self.balance = deposits['amount__sum'] - withdraws['amount__sum'] - checks['amount__sum']
        self.save()
        return self.balance

    def get_savings_balance(self):

        return self.saving_account.balance

    def get_checking_balance(self):

        return self.checking_account.balance

    def get_balance_by_user(self, Owner):
        account = self.objects.get(owner=Owner)
        return account.balance

    #Updates total amount of money in Savings and Checking Accounts
    def update_balance(self, Amount=None):
        #Filter objects by account
        if Amount:
            self.balance += Amount
        self.balance += self.saving_account.balance
        self.balance += self.checking_account.balance
        self.save()

    #Return the total amount of money that has been written via checks, access the expense of each check
    def get_check_total(self):
        check_total = 0
        total_checks = Check.objects.filter(owner=self)
        for check in total_checks:
            check_total += check.expense.amount

    def get_deposit_total(self):
        deposit_total = 0
        total_deposits = Deposit.objects.filter(owner=self)
        for deposit in total_deposits:
            deposit_total += deposit.amount
        return deposit_total

    def get_withdraw_total(self):
        total = 0
        withdraws = Withdraw.objects.filter(owner=self)
        for withdraw in withdraws:
            total += withdraw.amount
        return total

    def get_checking_account(self):
        return self.checking_account

    def get_savings_account(self):
        return self.saving_account

    #Methods to return all corresponding Expenses and Checks related to the specified account
    def get_all_expenses(self):
        expenses = Expense.objects.filter(owner=self)
        return expenses

    def get_all_checks(self):
        checks = Check.objects.filter(owner=self)
        return checks

    def __unicode__(self):
        return self.account_name


class Checking(models.Model):

    name = models.CharField(max_length=25, default="Users Checking")
    owner = models.ForeignKey(User,blank=False, null=True, on_delete=models.SET_NULL)
    balance = models.DecimalField(verbose_name="Checking Balance",decimal_places=2,max_digits=10,default=0.0)
    #owners_account = models.ForeignKey(Account)
    #Methods for Values in model

    def checks_Written(self):
        checks = Check.objects.count()
        return checks

    def get_checks_by_owner(self, Owner):
        account_owner = Account.objects.get(owner=Owner)
        checks = Check.objects.filter(owner=account_owner)

    def get_balance_by_owner(self, Owner):
        #Get account by the user, who is the owner.
        checking = Checking.objects.get(owner=Owner)
        return checking.balance

    def update_balance(self, Amount=None, Add=True, Sub=False):
        if Amount:
            if Add:
                self.balance += Amount
            if Sub:
                self.balance -= Amount
        self.save()

    def __unicode__(self):
        return self.name


class Saving(models.Model):

    owner = models.ForeignKey(User,blank=False, null=True, on_delete=models.SET_NULL)
    balance = models.DecimalField(verbose_name="Saving Balance", decimal_places=2, max_digits=10, default=0.0)
    #owners_account = models.ForeignKey(Account)
    name = models.CharField(max_length=25,default="Users Savings")

    #Call this method each time we update the overall account balance
    def update_balance(self, Amount=None, Add=True, Sub=False):
        if Amount:
            if Add:
                self.balance += Amount
            if Sub:
                self.balance -= Amount
        self.save()

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

    owner = models.ForeignKey('Account')
    amount = models.DecimalField(verbose_name="Expense Amount", decimal_places=2,max_digits=10, default=0.0)
    reason = models.TextField()
    date = models.DateField()
    checking_expense = models.BooleanField(default=True)
    saving_expense = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None):
        if self.checking_expense:
            self.owner.checking_account.update_balance(self.amount,Sub=True, Add=False)
        if self.saving_expense:
            self.owner.saving_account.update_balance(self.amount, Sub=True, Add=False)
        self.owner.update_balance()
        return super(Expense, self).save(force_insert, force_update, using)

    def __unicode__(self):
        return self.reason


#Checks owner is an Account, as compared to Accounts owner which is a User.
class Check(models.Model):

    count = 0

    def get_total_deficit(self):
        total = 0
        checks = Check.objects.all()
        for check in checks:
            total -= check.expense.amount
        return total

    owner = models.ForeignKey('Account')
    memo = models.TextField()
    payee = models.ForeignKey(Payee)
    date = models.DateTimeField()
    expense = models.ForeignKey(Expense)
    check_number = models.IntegerField(max_length=200,default=count + 1)

    def save(self, force_insert=False, force_update=False, using=None):
        self.owner.checking_account.update_balance(self.expense.amount, Sub=True, Add=False)
        self.owner.update_balance()
        return super(Check, self).save(force_insert, force_update, using)

    def __unicode__(self):
        return str(self.check_number)


class Deposit(models.Model):

    owner = models.ForeignKey('Account')
    checking_deposit = models.BooleanField(default=False)
    savings_deposit = models.BooleanField(default=True)
    amount = models.DecimalField(verbose_name="Deposit Amount", decimal_places=2, max_digits=20,default=0.0)
    date = models.DateTimeField()

    def get_total_income(self):
        total = 0
        deposits = Deposit.objects.all()
        for deposit in deposits:
            total += deposit.amount
        return total

    def save(self, force_insert=False, force_update=False, using=None):
        if self.checking_deposit:
            self.owner.checking_account.update_balance(self.amount, Add=True)
        if self.savings_deposit:
            self.owner.saving_account.update_balance(self.amount, Add=True)
        self.owner.update_balance()
        return super(Deposit, self).save(force_insert, force_update, using)

    def __unicode__(self):
        return str(self.amount)


class Withdraw(models.Model):
    owner = models.ForeignKey('Account')
    amount = models.DecimalField(verbose_name="Expense Amount", decimal_places=2,max_digits=10, default=0.0)
    date = models.DateTimeField()
    savings = models.BooleanField(default=False)
    checking = models.BooleanField(default=True)
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

    def save(self, force_insert=False, force_update=False, using=None):
        if self.checking:
            self.owner.checking_account.update_balance(self.amount, Add=False, Sub=True)
        if self.savings:
            self.owner.saving_account.update_balance(self.amount, Add=False,Sub=True)
        self.owner.update_balance()
        return super(Withdraw, self).save(force_insert, force_update, using)

    def __unicode(self):
        return self.location