from datetime import datetime
from django.shortcuts import redirect, render
from django.core.files.storage import default_storage

from PlantDP.models import *
from PlantDP.plant_diseases_model import PlantDiseases
from UserProfile.models import PredictHistory

# Create your views here.
def Home(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            context = {
                "disease": None
            }
            return render(request, 'home.html', context)

        elif request.method == 'POST':
            file = request.FILES['image-predict']
            with default_storage.open('predicts/image_predict.jpg', 'wb') as storage:
                storage.write(file.read()) 
            img_path = "./media/predicts/image_predict.jpg"

            model = PlantDiseases('plant_diseases_model_25_class_best_v2.h5')
            result = model.predict(img_path)
            print(result)
            if result > 0:
                disease = Disease.objects.get(id=2)
                predict_history = PredictHistory(
                    user = request.user,
                    predict_time= datetime.now(),
                    disease = disease
                )
                predict_history.image = request.FILES['image-predict']
                predict_history.save()
                context = {
                    "disease": disease,
                    "predicted_image": img_path
                }
            else:
                context = {
                    "disease": None,
                    "is_predicted": False,
                    "predicted_image": img_path
                }

            return render(request, 'home.html', context)
    else:
        return redirect('login')


def Diseases(request):
    if request.method == 'GET':
        diseases = Disease.objects.filter(status = False)
        plants = Plant.objects.all()
        context = {
            "plants": plants,
            "diseases": diseases
        }
        return render(request, 'diseases.html', context)
    
    if request.method == 'POST':
        plant_id = int(request.POST['plant'])
        disease_name = request.POST['search-name']
        diseases = Disease.objects.all()
        if plant_id == 0:
            diseases_filter = diseases.filter(name__icontains=disease_name)
        else:
            diseases_filter = diseases.filter(
                plant_id=plant_id, name__icontains=disease_name)
        plants = Plant.objects.all()

        print(diseases_filter)
        context = {
            "plants": plants,
            "diseases": diseases_filter
        }
        return render(request, 'diseases.html', context)


def DiseaseDetail(request, id):
    disease = Disease.objects.get(pk=id)
    print(disease.images.all())
    context = {
        "disease": disease
    }
    return render(request, 'disease-detail.html', context)

def DiseaseDetail(request, id):
    disease = Disease.objects.get(pk=id)
    context = {
        "disease": disease
    }
    return render(request, 'disease-detail.html', context)



def Products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        categories = Category.objects.all()
        context = {
            "categories": categories,
            "products": products
        }
        return render(request, 'products.html', context)

    if request.method == 'POST':
        category_id = int(request.POST['category_id'])
        product_name = request.POST['search-name']
        products_filter = Product.objects.filter(name__icontains=product_name)
        if category_id != 0:
            products_filter = products_filter.filter(category_id=category_id)
        categories = Category.objects.all()

        print(len(products_filter))
        context = {
            "categories": categories,
            "products": products_filter,
            "category_id": category_id
        }
        return render(request, 'products.html', context)



def ProductDetail(request, id):

    product = Product.objects.get(id=id)
    products = Product.objects.filter(category_id = product.category_id)

    context = {
        "product": product,
        "products": products
    }
    return render(request, 'product-detail.html', context)
