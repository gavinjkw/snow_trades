import bcrypt
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db.models import Count, Sum
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import stripe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
stripe.api_key = settings.STRIPE_SECRET_KEY


def landing(request):
    return render(request, 'store/landing.html')


def index(request):
    return render(request, 'store/index.html')


def process_reg(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/register")
    else:
        hash_password = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt())
        new_user = User.objects.create(
            first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], hashed_pass=hash_password)
        user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = new_user.id
        request.session['first_name'] = user[0].first_name
        request.session['email'] = user[0].email
        request.session['shopping_cart'] = []
        request.session['item_state'] = 0
        return redirect('/store')


def login_process(request):
    errors = User.objects.basic_validator_login(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = user[0].id
        request.session['first_name'] = user[0].first_name
        request.session['email'] = user[0].email
        request.session['shopping_cart'] = []

        request.session['item_state'] = 0
        return redirect('/store')


def login(request):
    if 'user_id' in request.session:

        if request.session['item_state'] == 0:
            recent_items = Item.objects.all().order_by('-created_at')
        if request.session['item_state'] == 1:
            recent_items = Item.objects.filter(
                category='snowboard').order_by('-created_at')
        if request.session['item_state'] == 2:
            recent_items = Item.objects.filter(
                category='Skiis').order_by('-created_at')
        if request.session['item_state'] == 3:
            recent_items = Item.objects.filter(
                category='Boots').order_by('-created_at')
        if request.session['item_state'] == 4:
            recent_items = Item.objects.filter(
                category='Bindings').order_by('-created_at')
        if request.session['item_state'] == 5:
            recent_items = Item.objects.filter(
                category='Apparel').order_by('-created_at')

        paginator = Paginator(recent_items, 5)
        
        page = request.GET.get('page')

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            items = paginator.page(paginator.num_pages)

        ids = request.session['shopping_cart']
        content = {
            'user': User.objects.get(id=request.session['user_id']),
            'items': items,
            'cart_count': Item.objects.filter(id__in=ids).count(),
        }
        print(request.session['shopping_cart'])
        return render(request, 'store/store.html', content)
    else:
        return redirect("/")


def logout(request):
    request.session.clear()
    return redirect("/")


def add_item(request):
    if 'user_id' in request.session:
        print(request.session['shopping_cart'])
        ids = request.session['shopping_cart']
        content = {
            'user': User.objects.get(id=request.session['user_id']),
            'cart_count': Item.objects.filter(id__in=ids).count(),
        }
        return render(request, 'store/add_item.html', content)
    else:
        return redirect("/")


def add_item_process(request):
    errors = Item.objects.basic_validator(request.POST, request.FILES)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/add_item')

    elif request.method == 'POST':
        image_one = request.FILES['image_one']
        adding_user = User.objects.get(id=request.session['user_id'])
        if 'image_three' in request.FILES and 'image_two' in request.FILES:
            image_two = request.FILES['image_two']
            image_three = request.FILES['image_three']
            new_item = Item.objects.create(make=request.POST['make'], model=request.POST['model'], size=request.POST['size'], price=request.POST['price'],
                                       category=request.POST['category'], image_one=image_one, image_two=image_two, image_three=image_three, added_by=adding_user, desc=request.POST['desc'])
        elif 'image_two' in request.FILES:
            image_two = request.FILES['image_two']
            new_item = Item.objects.create(make=request.POST['make'], model=request.POST['model'], size=request.POST['size'], price=request.POST['price'],
                                       category=request.POST['category'], image_one=image_one, image_two=image_two, added_by=adding_user, desc=request.POST['desc'])
        else:
            new_item = Item.objects.create(make=request.POST['make'], model=request.POST['model'], size=request.POST['size'], price=request.POST['price'],
                                       category=request.POST['category'], image_one=image_one, added_by=adding_user, desc=request.POST['desc'])

        print("NEW ITEM", new_item.make)
        return redirect('/store')
    else:
        print("didnt make it")
        return redirect('/store')


def add_cart_process(request):
    request.session['shopping_cart'].append(int(request.POST['item_id']))
    print(request.session['shopping_cart'])
    request.session.modified = True
    return redirect('/store')


def shopping_cart(request):
    if 'user_id' in request.session:
        ids = request.session['shopping_cart']
        count = Item.objects.filter(id__in=ids).count()
        if count < 1:
            request.session['cart_state'] = 1
            context = {
                'user': User.objects.get(id=request.session['user_id']),
                'cart_count': Item.objects.filter(id__in=ids).count(),
            }
            return render(request, 'store/cart.html', context)
        else:
            request.session['cart_state'] = 2
            temp_val = Item.objects.filter(id__in=ids).aggregate(Sum('price'))
            stripe_val = temp_val['price__sum'] * 100
            items = Item.objects.filter(id__in=ids)
            added_by = items[0].added_by.id
            print(added_by)
            context = {
                'user': User.objects.get(id=request.session['user_id']),
                'items': Item.objects.filter(id__in=ids),
                'cart_count': Item.objects.filter(id__in=ids).count(),
                'cart_total': Item.objects.filter(id__in=ids).aggregate(Sum('price')),
                'key': settings.STRIPE_PUBLISHABLE_KEY,
                'stripe_val': stripe_val,
                'seller': added_by
            }
            return render(request, 'store/cart.html', context)
    else:
        return redirect("/")


def complete_purchase(request):
    ids = request.session['shopping_cart']
    temp_val = Item.objects.filter(id__in=ids).aggregate(Sum('price'))
    stripe_val = int(temp_val['price__sum'])
    final_val = stripe_val * 100
    final_final_val = int(final_val)

    temp_buyer = User.objects.get(id=request.session['user_id'])
    temp_seller = User.objects.get(id=request.POST['seller_id'])
    new_order = Order.objects.create(
        total_price=stripe_val, buyer=temp_buyer, seller=temp_seller)
    
    for item in request.session['shopping_cart']:
        print("loop_item", item)
        temp_item = Item.objects.get(id=item)
        print("temp_item", temp_item)
        new_order.items.add(temp_item)
    print("ITEM", new_order.items.all())

    if request.method == "POST":
        token = request.POST.get("stripeToken")
        
    try:
        charge = stripe.Charge.create(
            amount=final_final_val,
            currency="usd",
            source=token,
            description="The product charged to the user"
        )

        new_order.charge_id = charge.id
        new_order.save()

    except stripe.error.CardError as ce:
        return False, ce

    else:
        request.session['shopping_cart'] = []
        request.session.modified = True
        new_order.save()
        return redirect ('/purchase_page')
        
        # The payment was successfully processed, the user's card was charged.
        # You can now redirect the user to another page or whatever you want

    return redirect('/store')

def purchase_page (request):
    ids = request.session['shopping_cart']
    order = Order.objects.latest('created_at')
    if 'user_id' in request.session:
       
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'cart_count': Item.objects.filter(id__in=ids).count(),
            'items': order.items.all(),
            'order': order
        }
        
        return render(request, 'store/order_done.html', context)
    else:
        return redirect("/")


def delete_cart_item(request):
    print("shopping Cart: ", request.session['shopping_cart'])
    print("item id:", request.POST['item_id'])
    request.session['shopping_cart'].remove(int(request.POST['item_id']))
    request.session.modified = True
    return redirect('/cart')


def home(request):
    request.session['item_state'] = 0
    return redirect('/store')


def snowboards(request):
    request.session['item_state'] = 1
    return redirect('/store')


def skiis(request):
    request.session['item_state'] = 2
    return redirect('/store')


def boots(request):
    request.session['item_state'] = 3
    return redirect('/store')


def bindings(request):
    request.session['item_state'] = 4
    return redirect('/store')


def apparel(request):
    request.session['item_state'] = 5
    return redirect('/store')


def account(request):
    if 'user_id' in request.session:
        ids = request.session['shopping_cart']
        user_items = Item.objects.filter(added_by__id=request.session['user_id']).order_by('-created_at')
        paginator = Paginator(user_items, 5)
        
        page = request.GET.get('page')

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            items = paginator.page(paginator.num_pages)


        context = {
            'user_items': items,
            'cart_count': Item.objects.filter(id__in=ids).count(),
        }

        return render(request, 'store/my_account.html', context)
    else:
        return redirect("/")

def edit_account(request):
    if 'user_id' in request.session:
        ids = request.session['shopping_cart']
        context = {
            'user_items': Item.objects.filter(added_by__id=request.session['user_id']).order_by('-created_at'),
            'user': User.objects.get(id=request.session['user_id']),
            'cart_count': Item.objects.filter(id__in=ids).count(),
        }

        return render(request, 'store/edit_account.html', context)
    else:
        return redirect("/")

def edit_user_process(request):
    errors = User.objects.basic_validator_edit(request.POST)
    if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
                print(errors)
     
            return redirect ('/edit_account')
    else:
        temp_user = User.objects.get(id=request.session['user_id'])
        temp_user.first_name = request.POST['first_name']
        temp_user.last_name = request.POST['last_name']
        temp_user.email = request.POST['email']
        temp_user.save()
        request.session['first_name'] = temp_user.first_name
        request.session['email'] = request.POST['email']
        print("new User Items:", temp_user.id, temp_user.first_name, temp_user.last_name, temp_user.email)
        return redirect('/account')

