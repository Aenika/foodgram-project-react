# Generated by Django 3.2.19 on 2023-06-24 07:16

from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230623_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=users.models.LowerEmailfield(max_length=254, verbose_name='Е-мейл'),
        ),
    ]
