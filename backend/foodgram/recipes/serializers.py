from base64 import b64decode
from uuid import uuid4
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from recipes.models import IngredientAmount, Tag, Ingredient, Recipe
from PIL import Image
from users.serializers import UsersSerializer



class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Tag
        
        
class IngregientsSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Ingredient
        

class IngredientAmountSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ['id', 'amount']
        model = IngredientAmount


class ImageSerializerField(serializers.ImageField):

    def to_internal_value(self, data):
        header, body = data.split(';base64,')
        file_format = header.split('image/')[-1]
        name = f'{uuid4()}.{file_format}'
        data = ContentFile(b64decode(body), name)
        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountSerializer(many=True)
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = ImageSerializerField()
    
    class Meta:
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorite',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        ]
        read_only_fields = ['author']
        model = Recipe
        
    def get_is_favorite(self, obj):
        return None

    def get_is_in_shopping_cart(self, obj):
        return None
    
    def to_internal_value(self, data):
        return super().to_internal_value(data)
    
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data) 
        for ingredient in ingredients: #TODO: сделать валидацию и удаление рецепта
            items = dict(ingredient)
            ingredient = IngredientAmount.objects.get_or_create(
                id=items['id'], amount=items['amount'])
            recipe.ingredients.add(ingredient[0].item_id)
        for tag in tags:
            tag = get_object_or_404(Tag, id=tag.id)
            recipe.tags.add(tag.id)
        return recipe


class TagGetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientAmountGetSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'name', 'measurement_unit', 'amount']
        model = IngredientAmount
        
    def get_name(self, obj):
        return obj.id.name
    
    def get_measurement_unit(self, obj):
        return obj.id.measurement_unit


class RecipeGetSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountGetSerializer(many=True)
    tags = TagGetSerializer(many=True)
    author = UsersSerializer()
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = ImageSerializerField()
    
    class Meta:
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorite',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        ]
        read_only_fields = ['author']
        model = Recipe
        
    def get_is_favorite(self, obj):
        return None

    def get_is_in_shopping_cart(self, obj):
        return None
    
    def to_internal_value(self, data):
        return super().to_internal_value(data)