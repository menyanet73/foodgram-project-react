from django.shortcuts import get_object_or_404, render
from djoser import views
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from users import serializers, models


class UserViewSet(views.UserViewSet):
    serializer_class = serializers.UsersSerializer
    
    def get_serializer_class(self):
        return serializers.UsersSerializer
    
    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.request.user
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)
    
    
class UsersView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        serializer = serializers.SignUpUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(
            models.User,
            username=request.data['username'])
        return Response(
            {
                'email': user.email,
                'id': user.pk,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            status=status.HTTP_200_OK
        )

class TokenCreateView(views.TokenCreateView):
    serializer_class = serializers.CustomTokenCreateSerializer