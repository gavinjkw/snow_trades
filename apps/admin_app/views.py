from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, timedelta
from .models import *


def index(request):

    return render(request, "admin_app/admin_login.html")

def login_admin(request):
    errors = User.objects.basic_validator_login_admin(request.POST)
    if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect ('/admin')
    else:
        user = User.objects.filter(email=request.POST['email'])  
        request.session['user_id'] = user[0].id
        request.session['first_name'] = user[0].first_name
        request.session['email'] = user[0].email
        request.session['access_level'] = user[0].access_level
        request.session['shopping_cart'] = []

        return redirect('/admin/home')


def login(request):
    if request.session['access_level'] != 3:
        return redirect ('/admin')
    else:   
        if 'state' not in request.session:
            request.session['state'] = 0
        how_many_days = 1
        count_24 = Order.objects.filter(created_at__gte=datetime.now()-timedelta(days=how_many_days)).count()

        how_many_days1 = 7
        count_7_days = Order.objects.filter(created_at__gte=datetime.now()-timedelta(days=how_many_days1)).count()

        context = {
            'orders': Order.objects.all().order_by('-created_at'),
            'items': Item.objects.all().order_by('-created_at'),
            'users': User.objects.all().order_by('-created_at'),
            'item_count': Item.objects.all().count(),
            'order_count': Order.objects.all().count(),
            'user_count': User.objects.all().count(),
            '24hr_order': count_24,
            '7day_order': count_7_days,
        }
        return render(request, "admin_app/admin_home.html", context)

def logout_admin(request):
    request.session.clear()
    return redirect ("/admin")

def items(request):
    request.session['state'] = 1
    return redirect ('/admin/home')

def orders(request):
    request.session['state'] = 0
    return redirect ('/admin/home')

def users(request):
    request.session['state'] = 2
    return redirect ('/admin/home')

def delete_item(request):
    item = Item.objects.get(id = request.POST['item_id'])
    item.delete()
    return redirect ('/admin/home')

def delete_order(request):
    order = Order.objects.get(id = request.POST['order_id'])
    order.delete()
    return redirect ('/admin/home')

def delete_user(request):
    order = Order.objects.get(id = request.POST['order_id'])
    order.delete()
    return redirect ('/admin/home')