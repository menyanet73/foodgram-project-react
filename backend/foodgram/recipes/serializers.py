from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.serializers import UsersSerializer

from recipes.fields import ImageSerializerField
from recipes.models import Ingredient, IngredientAmount, Recipe, Tag


class IngredientAmountCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientAmount
        fields = ['id', 'name', 'amount', 'measurement_unit']

    def get_id(self, obj):
        return obj.ingredient.id

    def validate_amount(self, amount):
        if not isinstance(amount, int):
            raise serializers.ValidationError('Amount must be a int')
        if amount <= 0:
            raise serializers.ValidationError('Amount must be more than 0')
        return amount


class IngredientAmountGetSerializer(IngredientAmountCreateSerializer):
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = IngredientAmount
        fields = ['id', 'name', 'measurement_unit', 'amount']

    def get_measurement_unit(self, obj):
        return obj.ingredient.name


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'name', 'color', 'slug']
        read_only_fields = ['name', 'color', 'slug']
        model = Tag


class IngregientsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountCreateSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    image = ImageSerializerField()

    class Meta:
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        ]
        read_only_fields = ['author', 'is_favorited', 'is_in_shopping_cart']
        model = Recipe

    def validate_cooking_time(self, field):
        if field < 1:
            raise serializers.ValidationError('Min 1 minute')
        return field

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance = super().create(validated_data)
        self.add_many_ingredients(instance, ingredients)
        return instance

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            instance.ingredients.clear()
            ingredients = validated_data.pop('ingredients')
            self.add_many_ingredients(instance, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = GetRecipeSerializer(instance, context=self.context)
        return serializer.data

    def add_many_ingredients(self, instance, ingredients):
        for ingredient in ingredients:
            ingredient_instance = get_object_or_404(
                Ingredient, id=ingredient['ingredient']['id']
            )
            ingredient = IngredientAmount.objects.get_or_create(
                ingredient=ingredient_instance,
                amount=ingredient['amount']
            )
            instance.ingredients.add(ingredient[0].id)


class GetRecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UsersSerializer()
    is_favorited = serializers.BooleanField()
    is_in_shopping_cart = serializers.BooleanField()
    ingredients = IngredientAmountGetSerializer(many=True)

    class Meta:
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        ]
        read_only_fields = ['author', 'is_favorited', 'is_in_shopping_cart']
        model = Recipe
