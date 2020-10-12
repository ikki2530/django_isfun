from django.shortcuts import render, redirect
from django.http import HttpResponse
# import usercreations form
from django.contrib.auth.forms import UserCreationForm
# import login, logout
from django.contrib.auth import authenticate, login, logout
#import models to create the queries
from .models import *
# forms
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory
# messages
from django.contrib import messages
# decorators for check if the user is logged in
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
# customize decorators
from .decorators import unauthenticated_user, allowed_users, admin_only

@unauthenticated_user
def registerPage(request):
    """Register a new user in the database"""
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("user:", user)
            username = form.cleaned_data.get('username')
            # show this message if the user was created successfully
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

"""
A decorator is a function that takes another function as a parameter,
loginPage is the parameter (view_func) for the unauthenticated_user
"""
@unauthenticated_user
def loginPage(request):
    """login for the users registered"""
    #check if the user was logged in
    # check if the form was submitted
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        # authenticate the user
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # send a message in case of password or user are incorrect
            messages.info(request, 'Username or password is incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    "logout users"
    logout(request)
    return redirect('login')


# juan1 has admin permissions
# juan2 has customer permissions
@login_required(login_url='login')
@admin_only
def home(request):
    # query for the orders and customers
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers, 'total_customers': total_customers,
    'total_orders': total_orders, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer']) 
def userPage(request):
    # query for the orders and customers
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    print("ORDERS:", orders)
    context = {'orders': orders, 'total_orders': total_orders,
    'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer']) 
def accountSettings(request):
    """Profile view"""
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    # post: means update the data
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # allowed users in products view
def products(request):
    # queries to use in the products.html
    products  = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # allowed users in customer view
def customer(request, pk_test):
    # query for specific customer, add a check if the ip doesn't exist
    customer = Customer.objects.get(id=pk_test)

    # orders of the customer
    orders = customer.order_set.all()
    order_count = orders.count()

    #filters
    # myFilter = OrderFilter(request.GET, queryset=orders)
    # orders = myFilter.qs

    context = {'customer':customer, 'orders': orders, 'order_count': order_count}
    return render(request, 'accounts/customer.html', context)


# CRUD
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # allowed users in createOrder view
def createOrder(request, pk):
    """crear ordenes"""
    # parent model, child model
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == "POST":
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            """Guardar la información en la base de datos"""
            formset.save()
            """redirect to the dashboard"""
            return redirect('/')
    context = {'formset': formset }
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # allowed users in updateOrder view
def updateOrder(request, pk):
    """actualizar una orden"""
    order = Order.objects.get(id=pk)
    """creating the instance with the pk specified"""
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            """Guardar la información en la base de datos"""
            form.save()
            """redirect to the dashboard"""
            return redirect('/')
    context = {'formset': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # allowed users in deleteOrder view
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)