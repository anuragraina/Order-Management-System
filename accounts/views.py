from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from .forms import OrderForm, CreationForm
from .filters import OrderFilter
from .decorators import *


@not_authenticated
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username OR password is incorrect!')

    return render(request, 'accounts/login.html')


@not_authenticated
def register(request):
    form = CreationForm()

    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_access
def dashboard(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()  
    total_orders = orders.count()
    delivered_orders = orders.filter(status='Delivered').count()
    pending_orders = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers, 'total_orders': total_orders,
               'delivered': delivered_orders, 'pending': pending_orders}

    return render(request, 'accounts/dashboard.html', context)


def user_page(request):
    return render(request, 'accounts/user.html')


@login_required(login_url='login')
@allow_access(user_types=['admin'])
def product(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
@allow_access(user_types=['admin'])
def customer(request, pk):
    display_customer = Customer.objects.get(id=pk)
    customer_orders = display_customer.order_set.all()
    total_orders = customer_orders.count()

    order_filter = OrderFilter(request.GET, queryset=customer_orders)
    customer_orders = order_filter.qs

    context = {'customer': display_customer, 'orders': customer_orders,
               'total_orders': total_orders, 'order_filter': order_filter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allow_access(user_types=['admin'])
def create_order(request, pk):
    order_form_set = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=10)

    customer_ref = Customer.objects.get(id=pk)
    formset = order_form_set(
        queryset=Order.objects.none(), instance=customer_ref)
#    form = OrderForm(initial={'customer': customer_ref})

    if request.method == 'POST':
        formset = order_form_set(request.POST, instance=customer_ref)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset, }
    return render(request, 'accounts/place_order.html', context)


@login_required(login_url='login')
@allow_access(user_types=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/place_order.html', context)


@login_required(login_url='login')
@allow_access(user_types=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order': order}
    return render(request, 'accounts/delete_order.html', context)
