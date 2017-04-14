from rest_framework import permissions


class CustomerIsAdminAccessPermission(permissions.IsAdminUser):
    message = '해당 요청에 대한 권한이 없습니다.'