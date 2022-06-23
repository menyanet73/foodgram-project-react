from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS


class IsAuthorOrAuthOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return bool(obj.author == request.user or
                    request.method in SAFE_METHODS)
