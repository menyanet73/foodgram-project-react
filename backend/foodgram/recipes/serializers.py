from base64 import b64decode
from uuid import uuid4

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.serializers import UsersSerializer

from recipes.models import Ingredient, IngredientAmount, Recipe, Tag


class IngredientAmountField(serializers.Field):
    
    def to_internal_value(self, data):
        return data
    
    def to_representation(self, value):
        result_list = []
        ingrediends_amount = value.instance.ingredients.all()
        for ingredient_amount in ingrediends_amount:
            result_list.append({
                'id': ingredient_amount.id.id,
                'name': ingredient_amount.id.name,
                'measurement_unit': ingredient_amount.id.measurement_unit,
                'amount': ingredient_amount.amount
            })
        return result_list


class TagField(serializers.Field):
    
    def to_internal_value(self, data):
        return data
    
    def to_representation(self, value):
        result_list = []
        tags = value.instance.tags.all()
        for tag in tags:
            result_list.append({
                'id': tag.id,
                'name': tag.name,
                'color': tag.color,
                'slug': tag.slug
            })
        return result_list
    

class ImageSerializerField(serializers.ImageField):
    
    def to_internal_value(self, data):
        header, body = data.split(';base64,')
        file_format = header.split('image/')[-1]
        name = f'recipes/images/{uuid4()}.{file_format}'
        data = ContentFile(b64decode(body), name)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Tag


class IngregientsSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountField()
    tags = TagField()
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
        
    def validate(self, attrs):
        if not isinstance(attrs['ingredients'], list):
            raise serializers.ValidationError('Ingredients must be a list')
        for ingredient in attrs['ingredients']:
            if not 'id' in ingredient or not 'amount' in ingredient:
                raise serializers.ValidationError(
                    'Ingredients must contain id and amount fields')
        if not isinstance(attrs['tags'], list):
            raise serializers.ValidationError('Tags must be a list of tags id')
        return super().validate(attrs)

    def get_is_favorite(self, obj):
        if self.context.get('request').user.id is None:
            return False
        return obj.favorites.filter(
            user=self.context.get('request').user).exists()

    def get_is_in_shopping_cart(self, obj):
        if self.context.get('request').user.id is None:
            return False
        return obj.cart.filter(user=self.context.get('request').user).exists()

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data) 
        for ingredient in ingredients: #TODO: сделать валидацию
            ingredient_instance = get_object_or_404(
                Ingredient, id=ingredient['id'])
            ingredient = IngredientAmount.objects.get_or_create(
                id=ingredient_instance, amount=ingredient['amount'])
            recipe.ingredients.add(ingredient[0].item_id)
        for tag in tags:
            tag = get_object_or_404(Tag, id=tag)
            recipe.tags.add(tag)
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in self.initial_data:
            for current_ingredient in instance.ingredients.all():
                instance.ingredients.remove(current_ingredient)
            ingredients = validated_data.pop('ingredients')
            for ingredient in ingredients: #TODO: сделать валидацию
                ingredient_instance = get_object_or_404(
                    Ingredient, id=ingredient['id'])
                ingredient = IngredientAmount.objects.get_or_create(
                    id=ingredient_instance, amount=ingredient['amount'])
                instance.ingredients.add(ingredient[0].item_id)
        if 'tags' in self.initial_data:
            for current_tag in instance.tags.all():
                instance.tags.remove(current_tag)
            tags = validated_data.pop('tags')
            for tag in tags:
                tag = get_object_or_404(Tag, id=tag.id)
                instance.tags.add(tag.id)
        return super().update(instance, validated_data)


class RecipeLiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']
