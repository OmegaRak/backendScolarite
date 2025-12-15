from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'ADMIN'

class IsCandidatUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'CANDIDAT'
