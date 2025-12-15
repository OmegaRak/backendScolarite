from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET',):
            return True
        return bool(request.user and request.user.is_authenticated and getattr(request.user,'role',None) == 'ADMIN')
