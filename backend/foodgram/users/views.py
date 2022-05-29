from django.shortcuts import get_object_or_404, render
from djoser import views
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from users import serializers, models
from users.viewsets import CreateListRetrieveViewset


class UserViewSet(CreateListRetrieveViewset):
    queryset = models.User.objects.all()
    serializer_class = serializers.UsersSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.SignUpUserSerializer
        else:
            return serializers.UsersSerializer

    def get_permissions(self):
        super().get_permissions()
        if self.action == 'create':
            permision_classes = [permissions.AllowAny,]
        else:
            permision_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permision_classes]

    @action(["get"], detail=False) #TODO: Доделать эндпоинт
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(models.User, id=request.user.pk)
        serializer = self.get_serializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
