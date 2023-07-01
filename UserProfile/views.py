import base64
import datetime
import requests
import json

from django.shortcuts import render, redirect
from django.http import JsonResponse
from PlantDP.models import Product
from UserProfile.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from UserProfile.models import Cart, CartItem, PredictHistory

clientID = 'AVSSyB0LNEiWAAfyElAfkbVqbIOcV4xEwwVYR--k6OF_iUfjZZGrDxpTzQtCxcoqPLU4AV4CTObg22Tx'
clientSecret = 'EHAM-N95NzEy0u7RlOKlyy5jTHDSwBqunV65z_8z680Hyf4MQo6DO9eNdj5LxbfqfFceC3iE63vTOWaD'


def Login(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home-page')
        messages.error(request, "Tài khoản hoặc mật khẩu không chính xác!")
        return redirect(request.path_info)

    if request.method == 'GET':
        return render(request, 'login.html')


def Logout(request):
    logout(request)
    return redirect('login')


def Register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Bạn đã tạo tài khoản thành công! Hãy đăng nhập tài khoản vừa tạo.")
            return redirect('login')
        
        error= ""
        for val in user_form.errors.values():
            error += val[0] +"\n"
        messages.error(request, error)
        return redirect('register')

@login_required
def EditProfile(request):
    if request.method == 'GET':
        return render(request, 'edit-profile.html')

    if request.method == 'POST':
        if len(request.FILES) > 0:
            avt_form = AvatarFrom(request.POST, request.FILES, instance= request.user)
            if avt_form.is_valid():
                avt_form.save()
                return redirect(request.path_info)
            
            error= ""
            for val in avt_form.errors.values():
                error += val[0] +"\n"
            messages.error(request, error)
            return redirect(request.path_info)
                  
        else:
            profile_form = ProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect(request.path_info)
            
            error= ""
            for val in profile_form.errors.values():
                error += val[0] +"\n"
            messages.error(request, error)
            
            return redirect(request.path_info)

def HistoryPage(request):
    histories = PredictHistory.objects.filter(user = request.user)
    print(histories)
    context ={
        'histories': histories
    }
    return render(request, 'history.html', context)

def ShoppingCartPage(request):
    try:
        isPaid = request.GET['isPaid']
    except:
        isPaid = "False"

    cart = Cart.objects.get(user_id = request.user.id) 
    context = {
            'cart': cart,
            'is_paid': True if isPaid == "True" else False
        }
    try: 
        if isPaid == "True":
            cartItems = cart.cart_items.filter(is_paid = True)
            context.update({'cart_items': cartItems})
        else:
            cartItems = cart.cart_items.filter(is_paid = False)
            context.update({ 'cart_items': cartItems})
    
        return render(request, 'shopping-cart.html',context)
    except:
        context.update({
            'cart_items': None,
            })
        return render(request, 'shopping-cart.html',context)
        

def UpdateCartItem(request):
    data = json.loads(request.body)
    cart = Cart.objects.get(user_id = request.user.id)

    if data['action'] == 'add':
        product_id = data['product_id']
        quantity = data['quantity']
        product = Product.objects.get(id = product_id)
        try:
            cartItemExist = CartItem.objects.get(product = product, cart = cart, is_paid = False)
            cartItemExist.quantity += quantity
            cartItemExist.save()

            cart.sub_price += product.price * quantity
            cart.save()
            
        except:
            CartItem.objects.create(
                cart = cart,
                product = product,
                quantity = quantity,
                price = product.price,        
            )
            cart.sub_price += product.price * quantity
            cart.item_quantity += 1
            cart.save()

        return JsonResponse({
            'message':'Thêm vào giỏ hàng thành công!',
            'cart_number': cart.item_quantity},
            safe= False)

    elif data['action'] == 'remove':
        cart_item_id = data['cart_item_id']
        try:
            cartItemExist = CartItem.objects.get(id = cart_item_id)
            cartItemExist.delete()
            return JsonResponse('Remove cart item is cuccess', safe= False)

        except:
            return JsonResponse('Can not remove cart item', safe= False)

    elif data['action'] == 'update':
        cart_item_id = data['cart_item_id']
        quantity = data['quantity']
        try:
            cartItemExist = CartItem.objects.get(id = cart_item_id)
            cartItemExist.quantity += quantity
            cartItemExist.save()

            cart.sub_price += cartItemExist.price * quantity
            cart.save()
            return JsonResponse('Remove cart item is cuccess', safe= False)

        except:
            return JsonResponse('Can not remove cart item', safe= False)


def CheckoutCartPage(request):
    if request.method == 'POST':	
        cart = Cart.objects.get(user_id= request.user.id)
        money = float(cart.TotalPrice) // 23000
        print(money)
        data = CreateOrder(cart)
        return JsonResponse(data)

def CapturedPage(request):
    if request.method == 'GET':	
        orderId = request.GET['orderId']
        data = CapturedPayment(orderId)
        cart = Cart.objects.get(user_id= request.user.id)
        cartItems = CartItem.objects.filter(cart = cart, is_paid = False)
        for cartItem in cartItems:
            cartItem.is_paid = True
            cartItem.checkout_time = datetime.datetime.now()
            cartItem.save()
        cart.sub_price = 0
        cart.item_quantity = 0
        cart.save()  
        return JsonResponse(data)




# Get token paypal

def GetToken():
    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    data = {
        "client_id": clientID,
        "client_secret": clientSecret,
        "grant_type": "client_credentials"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic {0}".format(base64.b64encode((clientID+ ":" + clientSecret).encode()).decode())
    }

    token = requests.post(url, data, headers=headers)
    return token.json()['access_token']

# Create a order to Paypal
def CreateOrder(cart):
    sub_price = 0
    shipping = float(cart.shipping_fee) // 23000
    cartItems = CartItem.objects.filter(cart=cart, is_paid=False)
    items = []
    for cartItem in cartItems:
        item = {}
        item["name"] = cartItem.product.name
        item["quantity"] = f"{cartItem.quantity}"
        price = float(cartItem.price)//23000
        sub_price += price * cartItem.quantity
        item["unit_amount"] = {
            "currency_code": "USD",
            "value": f"{price}"
        }
        items.append(item)
    total_price = sub_price + shipping
    token = GetToken()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
    }
    jsonData = {
        "intent": "CAPTURE",
        "application_context": {
            "brand_name": "Plant Pathology Company",
            "shipping_preference": "NO_SHIPPING",
            "user_action": "CONTINUE"
        },
        "purchase_units": [
            {
                "description": "Bạn đang thanh toán cho Plant Pathology Company.",
                "items": items,
                "amount": {
                    "currency_code": "USD",
                    "value": f"{total_price}",
                    "breakdown": {
                        "item_total": {
                            "currency_code": "USD",
                            "value": f"{sub_price}"
                        },
                        "shipping": {
                            "currency_code": "USD",
                            "value": f"{shipping}"
                        }
                    }
                }
            }
        ]
    }
    response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders',
                                headers=headers,
                                json=jsonData
                                )
    return response.json()

# Capture a order to Paypal
def CapturedPayment(orderId):
    token = GetToken()

    captureurl = f'https://api.sandbox.paypal.com/v2/checkout/orders/{orderId}/capture'#see transaction status
    headers = {
        "Content-Type": "application/json",
        'Authorization': 'Bearer ' + token,
        }
    response = requests.post(captureurl, headers=headers)
    return response.json()

