from rest_framework import permissions

def is_staff(user):
    return hasattr(user,'staff')

def is_member(user):
    return hasattr(user,'member')

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or is_staff(request.user)

class IsMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_member(request.user)

class DenyAll(permissions.BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False