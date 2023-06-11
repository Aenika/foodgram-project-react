# flake8: noqa: I001, I004
import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Заполняет базу данных данными из файла ingredients.csv"""
    help = 'Заполняет базу данных из файла ingredients.csv'

    def handle(self, *args, **options):
        with open(
            f'{settings.BASE_DIR}/data/ingredients.csv', encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            for ingredient in reader:
                Ingredient.objects.get_or_create(
                    name=ingredient[0],
                    measurement_unit=ingredient[1]
                )
