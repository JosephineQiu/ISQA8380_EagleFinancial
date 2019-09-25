from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm,LoginForm
from django.contrib.auth import authenticate,login
from django.http import HttpResponse

# Create your views here.

now = timezone.now()


def home(request):
    return render(request, 'portfolio/home.html',
                  {'portfolio': home})


@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request,
                  'portfolio/customer_list.html',
                  {'customers': customers})


@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)

   if request.method == "POST":
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           customers = Customer.objects.all()
           return render(request, 'portfolio/customer_list.html',
                         {'customers': customers})
   else:
        # edit
       form = CustomerForm(instance=customer)
   return render(request, 'portfolio/customer_edit.html', {'form': form})


@login_required
def customer_delete(request, pk):
     customer = get_object_or_404(Customer, pk=pk)
     customer.delete()
     return redirect('portfolio:customer_list')


@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            customer.updated_date=timezone.now()
            customer.save()
            customers = Customer.objects.all()
        return render(request,
                      'portfolio/customer_list.html',
                      {'customers': customers})
    else:
       form = CustomerForm()
       return render(request,
                     'portfolio/customer_create.html',
                     {'form': form})


@login_required
def stock_list(request):
   stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/stock_list.html', {'stocks': stocks})


@login_required
@login_required
def stock_new(request):
   if request.method == "POST":
       form = StockForm(request.POST)
       if form.is_valid():
           stock = form.save(commit=False)
           stock.created_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html',
                         {'stocks': stocks})
   else:
       form = StockForm()
       # print("Else")
   return render(request, 'portfolio/stock_new.html', {'form': form})



@login_required
def stock_edit(request,pk):
    stock = get_object_or_404(Stock, pk=pk)
    if request.method =='POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.recent_date = timezone.now()
            stock.save()
            stocks = Stock.objects.all()
        return render(request,
                      'portfolio/stock_list.html',
                      {'stocks':stocks})
    else:
      form=StockForm(instance=stock)
    return render(request,
                  'portfolio/stock_edit.html',
                  {'form': form,
                   'stock': stock,
                   'pk': pk,})


@login_required()
def stock_delete(request, pk):
     stock = get_object_or_404(Stock, pk=pk)
     stock.delete()
     return redirect('portfolio:stock_list')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('portfolio:home')
                else:
                    return HttpResponse('Sorry, the account is disabled')
            else:
                return HttpResponse('Invalid credentials')
    else:
        form = LoginForm()
    return render(request,
                  'accounts/login.html',
                  {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            return render(request,
                          'accounts/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'accounts/register.html',
                  {'user_form':user_form})

@login_required
def investment_list(request):
    investments = Investment.objects.all()
    return render(request,
                  'portfolio/investment_list.html',
                  {'investments':investments})

@login_required
def investment_edit(request,pk):
    investment=get_object_or_404(Investment,pk=pk)
    if request.method=='POST':
          form=InvestmentForm(request.POST,instance=investment)
          if form.is_valid():
              investment=form.save(commit=False)
              investment.pk=pk
              investment.save()
              investments=Investment.objects.all()
          return render(request,
                        'portfolio/investment_list.html',
                        {'pk':pk,
                         'investment':investment,
                         'investments':investments})
    else:
        form = InvestmentForm(instance=investment)
    return render(request,
                  'portfolio/investment_edit.html',
                {'form':form})

@login_required
def investment_create(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.recent_date = timezone.now()
            investment.save()
            investments = Investment.objects.all()
        return render(request,
                       'portfolio/investment_list.html',
                       {'investments':investments}
                       )
    else:
        form = InvestmentForm
    return render(request,
                    'portfolio/investment_create.html',
                        {'form': form})


@ login_required
def investment_delete(request,pk):
    investment = get_object_or_404(Investment,pk=pk)
    investment.delete()
    return redirect('portfolio:investment_list')


def logout(request):
    return render(request,
                  "accounts/logged_out.html")

