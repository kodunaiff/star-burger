# Generated by Django 4.2 on 2024-03-21 08:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0047_order_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderelements',
            name='quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='количество'),
        ),
    ]
