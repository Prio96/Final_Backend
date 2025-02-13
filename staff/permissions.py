from rest_framework import permissions
from .models import is_staff,is_member

class IsStaff(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_superuser or is_staff(request.user)

class IsMember(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return is_member(request.user)

class UpdateOwnDetails(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.member.user==request.user