from django.db.models import Sum
from django.shortcuts import get_object_or_404

from recipes.models import Dosage, Ingredient


def create_content(user):
    """
    Создает скачиваемый список покупок
    в формате: ингредиент — дозировка.
    """
    ingredients = Dosage.objects.filter(
        recipy__recipes_shoppingcarts__user=user
    ).values('ingredient').annotate(sum_amount=Sum('amount'))
    content = 'Необходимо купить: \n'
    for i in ingredients:
        ingredient = get_object_or_404(Ingredient, id=i['ingredient'])
        amount = i['sum_amount']
        content += (
            f'- {ingredient.name}'
            f' ({ingredient.measurement_unit})'
            f' — {amount};\n'
        )
    content += (
        '\n Спасибо, что воспользовались приложением от Вики'
        '\n https://github.com/Aenika'
    )
    return content
