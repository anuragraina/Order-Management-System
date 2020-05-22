from django.shortcuts import render
from .models import *


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    passing = {'orders': orders, 'customers': customers}

    return render(request, 'accounts/dashboard.html', passing)


def product(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def customer(request):
    return render(request, 'accounts/customer.html')
