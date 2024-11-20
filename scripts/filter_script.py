def create_filter(filter_path):
    filter_content = """from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import LimitOffsetPagination


class Filter:

    @staticmethod
    def _search(view, request, queryset):
        search_filter = SearchFilter()
        return search_filter.filter_queryset(request, queryset, view)

    @staticmethod
    def _ordering(view, request, queryset):
        ordering_filter = OrderingFilter()
        return ordering_filter.filter_queryset(request, queryset, view)

    @staticmethod
    def _filter_backend(request, queryset, view):
        filter_backend = DjangoFilterBackend()
        return filter_backend.filter_queryset(request, queryset, view)

    @staticmethod
    def _paginate(request, queryset):
        paginator = LimitOffsetPagination()
        return paginator.paginate(request, queryset)

    @classmethod
    def apply(cls, view, request, queryset):
        queryset = cls._search(view, request, queryset)
        queryset = cls._ordering(view, request, queryset)
        queryset = cls._filter_backend(request, queryset, view)
        return cls._paginate(request, queryset)

    @classmethod
    def apply_without_pagination(cls, view, request, queryset):
        queryset = cls._search(view, request, queryset)
        queryset = cls._ordering(view, request, queryset)
        return cls._filter_backend(request, queryset, view)
"""

    with open(filter_path, 'w') as file1:
        file1.write(filter_content)
        file1.close()
