from rest_framework.pagination import PageNumberPagination

class ClothPageNumberPagination(PageNumberPagination):
    page_size = 20