from rest_framework import exceptions, status


class NameDuplicationError(exceptions.APIException):
    """Создаёт исключение с форматом, ожидаемым фронтом."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        'ingredients': [{'ingredients': ['Дублируется ингредиент!']}]
    }
