from django.db import models

# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="static/plants")

    def __str__(self):
        return self.name


class Disease(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    cause = models.TextField()
    symptom = models.TextField()
    precautions = models.TextField()
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

class DiseaseImage(models.Model):
    image = models.ImageField(upload_to="static/diseases")
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name="images")

class Pesticide(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    producer = models.CharField(max_length=100)
    price = models.BigIntegerField()
    quantity = models.IntegerField()
    thumbnail = models.ImageField(upload_to='static/pesticides')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

class PesticideImage(models.Model):
    image = models.ImageField(upload_to="static/pesticides")
    pesticide = models.ForeignKey(Pesticide, on_delete=models.CASCADE)

