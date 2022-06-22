from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from users.models import Follow, User
from recipes.models import Recipe


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


class RecipeLiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class FollowResponseSerializer(UsersSerializer):
    recipes = RecipeLiteSerializer(many=True)
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

    # def get_recipes(self, obj):
        # serializer = GetRecipeSerializer()
        # return obj.recipes.all()

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = '__all__'

    def validate(self, attrs):
        if attrs['user'] == attrs['following']:
            raise serializers.ValidationError('Нельзя подписаться на себя')
        if Follow.objects.filter(
                user=attrs['user'], following=attrs['following']).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя')
        return super().validate(attrs)
