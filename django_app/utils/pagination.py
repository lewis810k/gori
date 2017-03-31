from rest_framework.pagination import CursorPagination


class TalentPagination(CursorPagination):
    page_size = 2
    ordering = 'tutor'
