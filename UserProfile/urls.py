from django.urls import path

from . import views

urlpatterns = [
    
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path("register/", views.Register, name="register"),
    path("edit-profile/", views.EditProfile, name="edit-profile"),
    path("history/", views.HistoryPage, name="history-page"),
    path("shopping-cart/", views.ShoppingCartPage, name="shopping-cart-page"),
    path("shopping-cart/update", views.UpdateCartItem, name="update-cart-page"),
    path("shopping-cart/checkout", views.CheckoutCartPage, name="checkout-page"),
    path("shopping-cart/capture/", views.CapturedPage, name="capture-page"),
]