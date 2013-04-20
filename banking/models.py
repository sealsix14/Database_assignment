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
    date_created = models.DateField(auto_now_add=True)

    def create_sub_accounts(self, Owner, account_name):
        #Create Savings and Checking account and save to the account with same owner.
        #We do this because we don't let the user set their own savings and checking accounts.
        saving = Saving()
        saving.owner = Owner
        saving.owners_account_id = self.id
        checking = Checking()
        checking.owner = Owner
        checking.owners_account_id = self.id
        s = saving.save()
        c = checking.save()
        return saving, checking

    #Gets account, calls self.objects.get() but encapsulates it into a method
    def get_account(self,Owner):
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
        total = deposits['amount__sum'] - withdraws['amount__sum'] - checks['amount__sum']
        return total

    def get_savings_balance(self):
        checks = Check.objects.filter(owner=self)
        withdraws = Withdraw.objects.filter(saving=True)
        deposits = Deposit.objects.filter(saving=True)
        checks = checks.aggregate(sum('amount'))
        withdraws = withdraws.aggregate(sum('amount'))
        deposits = deposits.aggregate(sum('amount'))
        total = checks['amount__sum'] - withdraws['amount__sum'] + deposits['amount__sum']
        return total

    def get_checking_balance(self):
        checks = Check.objects.filter(owner=self)
        withdraws = Withdraw.objects.filter(checking=True)
        deposits = Deposit.objects.filter(checking=True)
        checks = checks.aggregate(sum('amount'))
        withdraws = withdraws.aggregate(sum('amount'))
        deposits = deposits.aggregate(sum('amount'))
        total = checks['amount__sum'] - withdraws['amount__sum'] + deposits['amount__sum']
        return total

    def get_balance_by_user(self,Owner):
        account = self.objects.get(owner=Owner)
        return account.balance

    #Updates total amount of money in Savings and Checking Accounts
    def update_balance(self):
        self.checking_account.update_balance()
        self.saving_account.update_balance()
        self.balance += self.checking_account.balance
        self.balance += self.saving_account.balance

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
        withdraws=Withdraw.objects.filter(owner=self)
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

    def update_balance(self):
        this_account = Account.objects.get(owner=self.owner)
        checks = Check.objects.all()
        deposits = Deposit.objects.all()
        withdraws = Withdraw.objects.all()
        checks = checks.filter(owner=this_account)
        deposits = deposits.filter(owner=this_account)
        deposits = deposits.filter(checking_deposit=True)
        withdraws = withdraws.filter(owner=this_account)
        withdraws = withdraws.filter(checking=True)
        #Filter checks and deposits by Account
        for check in checks:
            if check.expense.amount > 0:
                self.balance -= check.expense.amount
        for deposit in deposits:
            if deposit.checking_deposit:
                self.balance += deposit.amount

    def __unicode__(self):
        return self.name


class Saving(models.Model):

    owner = models.ForeignKey(User,blank=False, null=True, on_delete=models.SET_NULL)
    balance = models.DecimalField(verbose_name="Saving Balance", decimal_places=2, max_digits=10, default=0.0)
    #owners_account = models.ForeignKey(Account)
    name = models.CharField(max_length=25,default="Users Savings")

    #Call this method each time we update the overall account balance
    def update_balance(self):
        account = Account.objects.get(owner=self.owner)
        expenses = Expense.objects.filter(saving_expense=True)
        expenses = expenses.filter(owner=account)
        for expense in expenses:
            self.balance -= expense.amount
        deposits = Deposit.objects.filter(savings_deposit=True)
        deposits = deposits.filter(owner=account)
        for deposit in deposits:
            self.balance += deposit.amount
        withdraws = Withdraw.objects.filter(owner=account)
        withdraws = withdraws.filter(savings=True)
        for withdraw in withdraws:
            self.balance -= withdraw.amount
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

    def save(self, *args, **kwargs):
        super(Check, self).save(*args, **kwargs) # Call the "real" save() method.
        account = Account.objects.get(owner=self.owner)
        account.update_balance()
        account.save()

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

    def save(self, *args, **kwargs):
        super(Deposit, self).save(*args, **kwargs) # Call the "real" save() method.
        account = Account.objects.get(owner=self.owner)
        account.update_balance()
        account.save()

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

    def save(self, *args, **kwargs):
        super(Withdraw, self).save(*args, **kwargs) # Call the "real" save() method.
        account = Account.objects.get(owner=self.owner)
        account.update_balance()
        account.save()

    def __unicode(self):
        return self.location