from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    Класс кастомной пагинации.
    Используется в api и users.
    """
    page_size = 6
    page_size_query_param = 'limit'
