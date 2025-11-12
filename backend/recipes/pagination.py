from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Кастомная пагинация с параметром limit."""

    page_size_query_param = "limit"
