import uuid
import json
import os
import requests

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
from . forms import *
from . models import *

# Create your views here.
def index(request):
    breakfast = Menu.objects.filter(breakfast=True)
    lunch = Menu.objects.filter(lunch=True)
    dinner = Menu.objects.filter(dinner=True)
    dessert = Menu.objects.filter(dessert=True)

    context = {
        'breakfast' : breakfast,
        'lunch': lunch,
        'dinner': dinner,
        'dessert': dessert,
    }

    return render(request, 'index.html', context)

def menu(request):
    menu = Menu.objects.all()

    context = {
        'menu':menu,
    }
    return render(request, 'menu.html', context)

@login_required(login_url='signin')
def details(request, id):
    detail = Menu.objects.get(pk=id)
    context = {
        'detail':detail,
    }

    return render(request,'details.html', context)

def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'message delivered')
            return redirect('contact')
    return render(request, 'contact.html')
            
def about(request):
    return render(request, 'about.html')
            
def services(request):
    return render(request, 'services.html')

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        phone = request.POST['phone']
        address = request.POST['address']
        state = request.POST['state']
        pix = request.POST['pix']
        form = SignupForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            newprofile = Profile(user=newuser)
            newprofile.first_name = newuser.first_name
            newprofile.last_name = newuser.last_name
            newprofile.email = newuser.email
            newprofile.phone = phone
            newprofile.address = address
            newprofile.state = state
            newprofile.pix = pix
            newprofile.save()
            login(request,newuser)
            messages.success(request,'Signup successfull')
            return redirect('index')
        else:
            messages.error(request, form.errors)
            return redirect('signup')
    return render(request, 'signup.html')

def signout(request):
    logout(request)
    return redirect('signin')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        passwrodd = request.POST['password']
        user = authenticate(request,username=username,password=passwrodd)
        if user is not None:
            login(request, user)
            messages.success(request,'Signin successful')
            return redirect('index')
        else:
            messages.error(request, 'Username/Password incorrect. Kindly supply correct details.')
            return redirect('signin')
    return render(request,'signin.html')

@login_required(login_url='signin')
def profile(request):
    profile = Profile.objects.get(user__username = request.user.username)

    context = {
        'profile':profile,
    }

    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def profile_update(request):
    profile=Profile.objects.get(user__username = request.user.username)
    update=ProfileUpdate(instance=request.user.profile)
    if request.method=='POST':
        update = ProfileUpdate(request.POST, request.FILES, instance= request.user.profile)
        if update.is_valid():
            update.save()
            messages.success(request,'Profile update successful')
            return redirect('profile')
        else:
            messages.error(request, update.errors)
            return redirect('profile_update')
    context = {
        'profile':profile,
        'update':update,
    }
    return render(request, 'profile_update.html',context)

@login_required(login_url='signin')
def password(request):
    form=PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request, 'Password Change Successful.')
            return redirect('profile')
        else:
            messages.error(request, form.errors)
            return redirect('password')

    context = {
        'form':form,
    }
    return render(request, 'password.html',context)

@login_required(login_url='signin')
def shopcart(request):
    if request.method == 'POST':
        quant = int(request.POST['quantity'])
        item_id= request.POST['menu_id']
        item = Menu.objects.get(pk=item_id)
        order_num = Profile.objects.get(user__username = request.user.username)
        cart_no = order_num.id

        cart = Shopcart.objects.filter(user__username = request.user.username, paid=False)
        if cart:
            basket= Shopcart.objects.filter(menu_id=item.id, user__username = request.user.username).first()
            if basket:
                basket.quantity += quant
                basket.amount = basket.price * quant
                basket.save()
                messages.success(request,'item added to Shopcart')
                return redirect('menu')
            else:
                newcart=Shopcart()
                newcart.user = request.user
                newcart.menu=item
                newcart.title_id=item.title
                newcart.quantity=quant
                newcart.price=item.price
                newcart.amount=item.price * quant
                newcart.order_no=cart_no
                newcart.paid=False
                newcart.save()
                messages.success(request,'item added to Shopcart')
                return redirect('menu')

        else:
            newcart=Shopcart()
            newcart.user = request.user
            newcart.menu=item
            newcart.name_id=item.title
            newcart.quantity=quant
            newcart.price=item.price
            newcart.amount=item.price * quant
            newcart.order_no=cart_no
            newcart.paid=False
            newcart.save()
            messages.success(request,'item added to Shopcart')
            return redirect('menu')

    return redirect('menu')

@login_required(login_url='signin')
def displaycart(request):
    trolley = Shopcart.objects.filter(user__username = request.user.username, paid=False)
    profile=Profile.objects.get(user__username = request.user.username)

    subtotal = 0
    vat = 0
    total = 0

    for item in trolley:
        subtotal += item.price * item.quantity

    vat = 0.075 * subtotal

    total = vat + subtotal

    context = {
        'trolley': trolley,
        'subtotal': subtotal,
        'vat': vat,
        'total': total,
        'profile':profile,
    }

    return render(request, 'displaycart.html', context)

@login_required(login_url='signin')
def deleteitem(request):
    item_id = request.POST['item_id']
    item_delete = Shopcart.objects.get(pk=item_id)
    item_delete.delete()
    messages.success(request, 'Item deleted successfully.')
    return redirect('displaycart')

@login_required(login_url='signin')
def increase(request):
    if request.method== 'POST':
        the_item = request.POST['itemid']
        the_quant = int(request.POST['quant'])
        modify = Shopcart.objects.get(pk=the_item)
        modify.quantity = the_quant
        modify.amount = modify.quantity * modify.price
        modify.save()
    return redirect('displaycart')

class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        summary = Shopcart.objects.filter(user__username = request.user.username, paid= False)
        subtotal = 0
        vat = 0
        total = 0

        for item in summary:
            subtotal += item.price * item.quantity

        vat = 0.075 * subtotal

        total = vat + subtotal

        context = {
            'tota':total,
            'summary':summary
        }
        return render(request, 'checkout.html', context)

def pay(request):
    if request.method == 'POST':
    # integrating to paystack
        api_key = 'sk_test_dac71c3c2296c265abff31ff5916f797a9658d02'
        curl = 'https://api.paystack.co/transaction/initialize'
        cburl = 'http://127.0.0.1:8000/callback'
        user= User.objects.get(username= request.user.username)
        email = user.email
        total = float(request.POST['total']) * 100
        cart_no = user.profile.id
        transac_code = str(uuid.uuid4())

        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference': transac_code, 'amount':int(total), 'email':email,
         'order_number':cart_no, 'callback_url':cburl, 'currecy': 'NGN'}

        try:
            r = requests.post(curl, headers=headers, json=data)
        except Exception:
            messages.error(request, 'Network busy, refresh and try again')
        else:
            transback = json.loads(r.text)
            rdurl = transback['data']['authorization_url']
            return redirect(rdurl)
        return redirect('displaycart')

def callback(request):
    profile=Profile.objects.get(user__username = request.user.username)
    basket= Shopcart.objects.filter(user__username = request.user.username, paid = False)

    for item in basket:
        item.paid = True
        item.save()

        stock = Menu.objects.get(pk = item.menu.id)
        stock.max_quantity -= item.quantity
        stock.save()

    context={
        'profile': profile,
    }
    return render(request, 'callback.html', context)
