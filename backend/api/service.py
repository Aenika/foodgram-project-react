import io

from django.db.models import Sum
from django.shortcuts import get_object_or_404
from recipes.models import Dosage, Ingredient
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))


def create_content(user):
    """
    Создает список покупок
    в формате: ингредиент — дозировка.
    """
    ingredients = Dosage.objects.filter(
        recipy__recipes_shoppingcarts__user=user
    ).values('ingredient').annotate(sum_amount=Sum('amount'))
    content = []
    content.append('Необходимо купить:')
    for i in ingredients:
        ingredient = get_object_or_404(Ingredient, id=i['ingredient'])
        amount = i['sum_amount']
        line = (
            f'- {ingredient.name}'
            f' ({ingredient.measurement_unit})'
            f' — {amount};'
        )
        content.append(line)
    return content


def create_downloadable_file(content):
    """Создаёт скачиваемый файл."""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    textobject = p.beginText()
    textobject.setTextOrigin(inch, 10 * inch)
    textobject.setFont("Arial", 14)
    for line in content:
        textobject.textLine(line)
    textobject.setFillGray(0.4)
    textobject.textLines('''
    Спасибо, что воспользовались приложением от Вики
    https://github.com/Aenika
    ''')
    p.drawText(textobject)
    p.showPage
    p.save()
    buffer.seek(0)
    return buffer
