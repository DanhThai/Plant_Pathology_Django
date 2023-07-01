
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from .managers import CustomUserManager
from PlantDP.models import Disease, Product


class CustomUser(AbstractUser):
    username = None
    first_name = None
    last_name = None
    
    email = models.EmailField(unique=True)
    full_name = models.CharField( max_length=100)
    address = models.CharField(max_length=256, blank=True, null= True)
    age = models.IntegerField(blank=True, null= True)
    phone_number = models.CharField(max_length=10, unique=True)
    avatar = models.ImageField(upload_to="avatars",max_length=100, null= True, blank= True)
    # paypal_account = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class PredictHistory(models.Model):
    image = models.ImageField(max_length=256, upload_to="predicts")
    status = models.BooleanField(default=False)
    predict_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete= models.CASCADE)

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete= models.CASCADE, primary_key= True, related_name="cart")
    shipping_fee = models.IntegerField(default=0)
    sub_price = models.IntegerField(default=0)
    item_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.full_name

    @property
    def TotalPrice(self):
        return (self.shipping_fee + self.sub_price)

class CartItem(models.Model):
    is_paid = models.BooleanField(default=False)
    delivered_time = models.DateTimeField(null= True, blank=True)
    checkout_time = models.DateTimeField(null= True, blank=True)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete= models.CASCADE)

    def __str__(self):
        return self.Product.name
    
    @property
    def PesticideName(self):
        return  self.pesticide.name

# method for updating
@receiver(post_save, sender=CustomUser)
def CreateCart(sender, instance, **kwargs):
    cart = Cart.objects.filter(user_id=instance.id)
    if cart.count() == 0 and not instance.is_staff:
        Cart.objects.create(user_id=instance.id)

# method for updating
@receiver(pre_delete, sender=CartItem)
def DeleteCartItem(sender, instance, **kwargs):
    instance.cart.item_quantity -= 1
    instance.cart.sub_price -= instance.price * instance.quantity
    instance.cart.save()