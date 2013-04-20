# Create your views here.
from django.shortcuts import *
from django.contrib.auth.models import User
from banking.forms import *
from django.core.context_processors import csrf
from django.contrib.auth.views import login
from banking.models import *

def home(request):
    template = 'home.html'
    user = request.GET.get('user')
    checks = Check.objects.all()
    return render_to_response(template, {'checks': checks, 'User': user}, context_instance=RequestContext(request))


def login(request):
    template = 'login.html'
    if request.user.is_authenticated:
        HttpResponseRedirect('/')
    else:
        login(request)
    return render_to_response(template,context_instance=RequestContext(request))

#View to create an account, acts as our registration form
# basically you enter your name,email, password, then we generate a user, along with an account,savings,and checking.
# with a balance of 0.0 for everything and no checks or deposits related to your account.
def add_account(request):
    template = 'add_account.html'
    if request.user.is_authenticated:
        HttpResponseRedirect("/")
        account = AccountForm()
    else:
        if request.method == 'POST':
            account = AccountForm(request.POST)
            if account.is_valid:
                account.save()
            else:
                account = AccountForm()
        else:
            account = AccountForm()

    return render_to_response(template, {'form': account}, context_instance=RequestContext(request))


def add_check(request):
    template = 'add_check.html'
    if request.user.is_authenticated:
        if request.method == 'POST':
            check_form = CheckForm(request.POST)
            if check_form.is_valid:
                check = check_form.save()
        else:
            check_form = CheckForm()
    else:
        check_form = CheckForm()
        HttpResponseRedirect("/accounts/login")

    return render_to_response(template, {'form': check_form, 'errors': check_form.errors},
                              context_instance=RequestContext(request))


def add_expense(request):
    template = 'add_expense.html'
    form = ExpenseForm()
    if request.POST:
        account = Account.objects.get(account_user=request.user)
        account.account_user = request.user
        form = ExpenseForm(request.POST)
        print account.account_user

        if form.is_valid():
            form.save()
        else:
            HttpResponseRedirect('/')
    expenses = Expense.objects.all()
    return render_to_response(template,{'form': form},
                              context_instance=RequestContext(request))


def add_deposit(request):

    if request.POST:
        deposit_form = DepositForm(request)
        deposit_form.is_valid()
    else:
        deposit_form = DepositForm()


def add_payee(request):

    template = "add_payee.html"
    if request.method == 'POST':
        p = PayeeForm(request.POST)
        if p.is_valid():
            p.save()
            HttpResponseRedirect("/")
    else:
        p = PayeeForm()
    return render_to_response(template, {'form': p}, context_instance=RequestContext(request))


def overview(request):
    template = "overview.html"
    account = Account.objects
    if request.user.is_authenticated:
        user = User.objects.get(request.user)
        account = account.get(owner=user)
        balance = account.balance
        saving_balance = account.saving_account.balance
        checking_balance = account.checking_account.balance
        checks = Check.objects.filter(owner=account)
        expenses = Expense.objects.filter(owner=account)
        return render_to_response(template, {'account':account,'account_balance': balance, 'saving_balance':saving_balance,
                                             'checking_balance':checking_balance,'checks': checks, 'expenses': expenses},
                                  context_instance=RequestContext(request))
    else:
        HttpResponseRedirect('/')