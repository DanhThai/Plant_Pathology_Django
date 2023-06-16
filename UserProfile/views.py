import base64
import datetime
import requests
import json

from django.shortcuts import render, redirect
from django.http import JsonResponse
from UserProfile.forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from UserProfile.models import Cart, CartItem

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
            return redirect('login')
        
        error= ""
        for val in user_form.errors.values():
            error += val[0] +"\n"
        messages.error(request, error)
        return redirect('register')


def ShoppingCartPage(request):
    try:
        isPaid = request.GET['isPaid']
    except:
        isPaid = False

    cart = Cart(user_id = 1, shipping = 15000, sub_price = 190000)
    cartItems = []
    for i in range(5):
        cartItem = CartItem(
            id= i,
            is_paid = False,
            delivered_time = datetime.datetime.now().__format__('%d/%m/%Y %H:%M:%S'),
            checkout_time = datetime.datetime.now().__format__('%d/%m/%Y %H:%M:%S'),
            quantity = 3, 
            price = 50000,
            cart = cart
        )
        cartItems.append(cartItem)
    context = {
            'cart': cart,
            'cart_items': cartItems
        }
    if isPaid == "True":
        context.update({'is_paid': True})
    else:
        context.update({'is_paid': False})
    
    return render(request, 'shopping-cart.html',context)

def UpdateCartItem(request, id):
    data = json.loads(request.data)
    if data['method'] == 'add':
        pass
    elif data['method'] == 'remove':
        pass
    elif data['method'] == 'update':
        pass


def CheckoutCartPage(request, cart_id):
    if request.method == 'POST':	
        # cart = Cart.objects.get(id=cart_id)
        # money = cart.total_price // 23000
        
        money = int(json.loads(request.body)['totalPrice']) // 23000
        print(money)
        data = CreateOrder(money)
        print(data)
        return JsonResponse(data)

def CapturedPage(request):
    if request.method == 'GET':	
        orderId = request.GET['orderId']
        data = CapturedPayment(orderId)
        print(data)
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
def CreateOrder(money):
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
                "amount": {
                    "currency_code": "USD",
                    "value": f"{money}"
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

