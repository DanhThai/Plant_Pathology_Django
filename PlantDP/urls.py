from django.urls import path

from . import views

# Create your views here.
urlpatterns = [
    path("home/", views.Home, name="home-page"),
    path("diseases/", views.Diseases, name="diseases-page"),
    path("diseases/<int:id>/", views.DiseaseDetail, name="disease-detail-page"),
    path("pesticides/", views.Pesticides, name="pesticides-page"),
    path("pesticides/<int:id>/", views.PesticideDetail, name="pesticide-detail-page"),
]