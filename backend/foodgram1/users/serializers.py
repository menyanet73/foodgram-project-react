from rest_framework import serializers
from users.models import User


class SignUpUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')

    def validate_username(self, username):
        pass
    #TODO: Сделать валидацию - символов не меньше, уникальное

class TokenCreateSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()
    
    class Meta:
        model = User
        fields = ('email', 'password')