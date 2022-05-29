from djoser.serializers import TokenCreateSerializer
from rest_framework import serializers
from users.models import User
from djoser.serializers import TokenCreateSerializer
from foodgram import settings


class SignUpUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует.'
            )
        return username
            

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return email
        

class UsersSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        return self.context['request'].user in obj.following.all()
    
class CustomTokenCreateSerializer(TokenCreateSerializer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields[settings.LOGIN_FIELDS] = serializers.CharField()