from django.db import models
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="plants", null= True, blank=True)

    def __str__(self):
        return self.name


class Disease(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=False, blank=True)
    cause = models.TextField(null= True, blank= True)
    symptom = models.TextField(null= True, blank= True)
    precautions = models.TextField(null= True, blank= True)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class DiseaseImage(models.Model):
    image = models.ImageField(upload_to="diseases")
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name="images")
    def __str__(self):
        return self.disease.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    item_quantity = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    brand = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    price = models.BigIntegerField()
    thumbnail = models.URLField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    image = models.URLField(max_length=256)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    def __str__(self):
        return self.product.name

# method for updating
@receiver(post_save, sender=Product)
def CreateProduct(sender, instance, **kwargs):
    instance.category.item_quantity +=1
    instance.category.save()