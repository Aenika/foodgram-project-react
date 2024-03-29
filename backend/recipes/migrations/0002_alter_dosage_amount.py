# Generated by Django 3.2.19 on 2023-06-22 21:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dosage',
            name='amount',
            field=models.IntegerField(help_text='Введите необходимое количество ингредиента', validators=[django.core.validators.MinValueValidator(0, 'Введите количество 1 или более!')], verbose_name='Количество'),
        ),
    ]
