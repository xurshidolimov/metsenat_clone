from rest_framework import pagination
from rest_framework.response import Response


class MyPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'list'
    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'all_object_count': self.page.paginator.count,
            'page_objects_count': len(self.page.object_list),
            'page_number': self.page.number,
            'all_pages_count': self.page.paginator.num_pages,
            'results': data
        })
