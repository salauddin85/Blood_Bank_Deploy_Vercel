from rest_framework.permissions import BasePermission

class Isadmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
    
class IsDonor(BasePermission):
    def has_permission(self, request, view):
        return request.user and not request.user.is_staff
