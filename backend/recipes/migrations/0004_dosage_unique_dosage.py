# Generated by Django 3.2.19 on 2023-06-24 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_remove_dosage_unique_dosage'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='dosage',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipy'), name='unique_dosage'),
        ),
    ]
