from django.urls import path

from . import views

# Create your views here.
urlpatterns = [
    path("", views.Home, name="home-page"),
    path("diseases/", views.Diseases, name="diseases-page"),
    path("diseases/<int:id>/", views.DiseaseDetail, name="disease-detail-page"),
    path("products/", views.Products, name="products-page"),
    path("products/<int:id>/", views.ProductDetail, name="product-detail-page"),
]