from django.shortcuts import get_object_or_404
from djoser import views
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from users import  models


class UserViewSet(views.UserViewSet):
    http_method_names = ['get', 'post']

    def get_permissions(self):
        super().get_permissions()
        if self.action == 'create':
            permision_classes = [permissions.AllowAny,]
        else:
            permision_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permision_classes]

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        user = get_object_or_404(
            models.User, username=request.data['username'])
        return Response(
            {
                "email": user.email,
                "id": user.pk,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }, status=status.HTTP_200_OK
        )

    @action(['get'], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)
