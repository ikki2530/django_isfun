from django.shortcuts import render, redirect
from django.http import HttpResponse
#import models to create the queries
from .models import *
# forms
from .forms import OrderForm
from django.forms import inlineformset_factory


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

def products(request):
    # queries to use in the products.html
    products  = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})

def customer(request, pk_test):
    # query for specific customer, add a check if the ip doesn't exist
    customer = Customer.objects.get(id=pk_test)

    # orders of the customer
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer':customer, 'orders': orders, 'order_count': order_count}
    return render(request, 'accounts/customer.html', context)


# CRUD
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
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)