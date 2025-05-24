from rest_framework.permissions import BasePermission

class IsServiceProvider(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and request.user.is_service_provider