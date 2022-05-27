from django.shortcuts import render
from djoser import views
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from users import serializers, viewsets, models


class UserViewSet(viewsets.CreateListRetrieveViewset):
    queryset = models.User.objects.all()
    serializer_class = serializers.UsersSerializer
    
    
    
class UsersView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        serializer = serializers.SignUpUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'email'
                'id'
                'username'
                'first_name'
                'last_name'
            },
            status=status.HTTP_200_OK
        )

# class TokenCreateView(views.TokenCreateView):
    # serializer_class = 