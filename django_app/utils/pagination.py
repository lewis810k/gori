from rest_framework.pagination import CursorPagination

__all__ = (
    'TalentPagination',
    'RegistrationPagination',
)


class TalentPagination(CursorPagination):
    page_size = 2
    ordering = 'created_date'


class RegistrationPagination(CursorPagination):
    page_size = 2
    ordering = 'joined_date'
