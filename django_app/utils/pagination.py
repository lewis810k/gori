from rest_framework.pagination import CursorPagination, LimitOffsetPagination, PageNumberPagination

__all__ = (
    'TalentPagination',
    'RegistrationPagination',
)


class TalentPagination(LimitOffsetPagination):
    page_size = 2
    ordering = 'created_date'


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class RegistrationPagination(CursorPagination):
    page_size = 2
    ordering = 'joined_date'
