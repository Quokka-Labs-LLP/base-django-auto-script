def create_pagination(pagination_path):
    pagination_content = """
from rest_framework.pagination import PageNumberPagination as DRFPagination


class LimitOffsetPagination(DRFPagination):
    page_size_query_param = 'limit'
    page_size = 10

    def paginate(self, request, queryset):
        data = self.paginate_queryset(queryset, request)
        pagination_data = {
            'total': self.page.paginator.count,
            'page': self.page.number,
            'limit': self.get_page_size(self.request),
            'totalPages': self.page.paginator.num_pages,
            'hasNextPage': self.page.has_next(),
            'hasPrevPage': self.page.has_previous(),
        }
        return data, pagination_data
"""

    with open(pagination_path, 'w') as file1:
        file1.write(pagination_content)
        file1.close()
