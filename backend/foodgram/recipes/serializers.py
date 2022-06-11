from base64 import b64decode
from uuid import uuid4
from django.core.files.base import ContentFile
from rest_framework import serializers
from recipes.models import IngredientAmount, Tag, Ingredient, Recipe
from PIL import Image



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
        super().to_internal_value(data)
    

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
        ingredients_list = []
        for ingredient in ingredients:
            items = dict(ingredient)
            ingredient = IngredientAmount.objects.create(
                id=items['id'], amount=items['amount'])
            ingredients_list.append(ingredient)
                
        recipe = Recipe.objects.create(
            ingredients=ingredients_list, **validated_data)
        return recipe
