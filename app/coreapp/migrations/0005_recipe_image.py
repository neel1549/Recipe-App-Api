# Generated by Django 2.1.15 on 2020-05-17 00:59

import coreapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0004_recipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(null=True, upload_to=coreapp.models.recipe_image_file_path),
        ),
    ]