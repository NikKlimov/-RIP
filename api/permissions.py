from rest_framework.permissions import BasePermission
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role=='MO'
    


class ReadOnly(BasePermission):    
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS