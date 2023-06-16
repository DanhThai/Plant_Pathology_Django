
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from .managers import CustomUserManager
from PlantDP.models import Disease, Pesticide


class CustomUser(AbstractUser):
    username = None
    first_name = None
    last_name = None
    
    email = models.EmailField(unique=True)
    full_name = models.CharField( max_length=100)
    address = models.CharField(max_length=256, blank=True, null= True)
    age = models.IntegerField(blank=True, null= True)
    phone = models.CharField(max_length=10, unique=True)
    avatar = models.ImageField(upload_to="static/avatars",max_length=100, null= True)
    # paypal_account = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class PredictHistory(models.Model):
    status = models.BooleanField(default=False)
    predict_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    predict = models.ForeignKey(Disease, on_delete= models.CASCADE)

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete= models.CASCADE, primary_key= True)
    shipping = models.IntegerField(default=0)
    sub_price = models.IntegerField(default=0)
    item_quantity = models.PositiveIntegerField(default=0)

    @property
    def TotalPrice(self):
        return (self.shipping + self.sub_price)

class CartItem(models.Model):
    is_paid = models.BooleanField(default=False)
    delivered_time = models.DateTimeField(auto_now= True)
    checkout_time = models.DateTimeField(auto_now= True)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE)
    pesticide = models.ForeignKey(Pesticide, on_delete= models.CASCADE)

    @property
    def PesticideName(self):
        return  self.pesticide.name

# method for updating
@receiver(post_save, sender=CartItem)
def update_stock(sender, instance, **kwargs):
    if instance.is_paid == False:
        instance.cart.item_quantity += 1
    else:
        instance.cart.item_quantity -= 1
    instance.cart.save()