# Generated by Django 4.1.3 on 2023-06-25 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("PlantDP", "0003_rename_producer_product_brand_product_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="thumbnail",
            field=models.URLField(max_length=256),
        ),
    ]
