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

def add_account(request):
    template = 'add_account.html'
    if request.POST:
        user = User.objects.create_user(request)
        user.validate_unique()
        user.save()
        HttpResponseRedirect('home.html')
    else:
        user = User()
    return render_to_response(template, {'user': user}, context_instance=RequestContext(request))


def add_check(request):
    template = 'add_check.html'
    if request.POST:
        check_form = CheckForm(request)
    else:
        check_form = CheckForm()

    return render_to_response(template, {'check': check_form, 'check_errors': check_form.errors},
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
    return render_to_response(template,{'expenses': expenses, 'accounts':Account.objects.all()},
                              context_instance=RequestContext(request))


def add_deposit(request):
   if request.POST:
       deposit_form = DepositForm(request)
       deposit_form.is_valid()
   else:
       deposit_form = DepositForm()


def overview(request):
    template = "overview.html"
    account = Account.objects
    if request.user.is_authenticated:
        account = account.get(account_user=request.user)
        balance = account.balance
        saving_balance = account.saving_account.saving_balance
        checking_balance = account.checking_account.checking_balance
        checks = Check.objects.filter(owner=account)
        expenses = Expense.objects.filter(owner=account)
    else:
        HttpResponseRedirect('/')
    return render_to_response(template, {'account':account,'account_balance': balance, 'saving_balance':saving_balance,
                                        'checking_balance':checking_balance,'checks': checks, 'expenses': expenses},
                                            context_instance=RequestContext(request))