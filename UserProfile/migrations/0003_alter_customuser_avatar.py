# Generated by Django 4.1.3 on 2023-06-25 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("UserProfile", "0002_rename_phone_customuser_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="avatar",
            field=models.ImageField(blank=True, null=True, upload_to="avatars"),
        ),
    ]
