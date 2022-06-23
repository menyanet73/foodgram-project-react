from django.contrib.auth.password_validation import validate_password
from recipes.models import Recipe
from rest_framework import serializers

from users.models import Follow, User


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={"input_type": "password"})
    current_password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        if attrs['new_password'] == attrs['current_password']:
            raise serializers.ValidationError(
                'Can not change to same password')
        return super().validate(attrs)

    def validate_new_password(self, new_password):
        user = self.context["request"].user or self.user
        try:
            validate_password(new_password, user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(
                {"new_password": list(e.messages)})
        return new_password

    def validate_current_password(self, value):
        if self.context["request"].user.check_password(value):
            return value
        else:
            raise serializers.ValidationError('Incorrect current password')


class UsersSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password'
        ]

    def get_is_subscribed(self, obj):
        if not self.context.get('request').user.is_authenticated:
            return False
        followers = self.context['request'].user.follower
        return followers.filter(following=obj).exists()

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = super().create(validated_data)
        instance.set_password(password)
        instance.save()
        return instance

    def validate_username(self, username):
        if len(username) < 3:
            raise serializers.ValidationError(
                'Username must be 3 chars minimum')
        return username


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
