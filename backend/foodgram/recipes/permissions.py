from rest_framework import permissions

permissions.IsAuthenticated
permissions.IsAdminUser

class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user