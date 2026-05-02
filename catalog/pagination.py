from rest_framework.pagination import PageNumberPagination


class FlexiblePageNumberPagination(PageNumberPagination):
    """Allow ?page_size= up to max_page_size (admin lists need full catalog)."""

    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 500
