from django.urls import path

from . import views

urlpatterns = [
    
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path("register/", views.Register, name="register"),
    path("shopping-cart/", views.ShoppingCartPage, name="shopping-cart-page"),
    path("shopping-cart/checkout/<int:cart_id>/", views.CheckoutCartPage, name="checkout-page"),
    path("shopping-cart/capture/", views.CapturedPage, name="capture-page"),
]