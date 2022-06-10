from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens 
from users import serializers, models


class SignUpUserView(APIView):
    
    def post(self, request):
        serializer = serializers.SignUpUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        id = serializer.validated_data.get('id')
        first_name = serializer.validated_data.get('first_name')
        last_name = serializer.validated_data.get('last_name')
        serializer.save()
        return Response(
            {
                'email': email,
                'id': id,
                'username': username,
                'first_name': first_name,
                'last_name': last_name
            },
            status=status.HTTP_200_OK
        )


class CreateUserToken(APIView):
    
    def post(self, request):
        serializer = serializers.TokenCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            models.User, email=serializer.validated_data['email'])
        if serializer.validated_data['password'] != user.password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        auth_token = 