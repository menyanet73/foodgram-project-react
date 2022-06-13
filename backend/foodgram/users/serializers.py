from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators
from users.models import User, Follow
from djoser.serializers import UserCreateSerializer


class SignUpUserSerializer(UserCreateSerializer):
    
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
        if self.context.get('request').user.id is None:
            return False
        followers = self.context['request'].user.follower
        return followers.filter(following=obj).exists()


class FollowSerializer(UsersSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count')
        
    def get_recipes(self, obj):
        return obj.recipes.all()
    
    def get_recipes_count(self, obj):
        return obj.recipes.all().count()
    
class FollowCreateSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Follow
        fields = '__all__'

    def validate_following(self, following):
        if self.context.get('request').method != 'POST':
            return following
        if self.context.get('request').user == following:
            raise serializers.ValidationError('Нельзя подписаться на себя')
        return following
