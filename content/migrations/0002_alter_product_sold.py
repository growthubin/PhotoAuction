# Generated by Django 4.2 on 2023-05-04 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product", name="sold", field=models.TextField(default=False),
        ),
    ]
