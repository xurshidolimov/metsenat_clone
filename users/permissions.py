from rest_framework import permissions


class CustomPermissions(permissions.IsAdminUser):
    pass
