import json

from PlantDP.models import Product, ProductImage

class InsertData():
    products_data = json.load(open("./Data/products_data.json", encoding='utf8'))

    for product_data in products_data:
        product = Product.objects.create(
            name=product_data["name"],
            description = product_data["description"],
            brand = product_data["brand"],
            type = product_data["type"],
            thumbnail = product_data["thumbnail"],
            price = product_data["price"],
            category_id = product_data["category_id"])
        
        images_data = product_data["images"]
        for img_link in images_data:
            img = ProductImage.objects.create(product = product, image = img_link)
