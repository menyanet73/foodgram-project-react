from django.shortcuts import render
from rest_framework import viewsets
from recipes import serializers
from recipes.viewsets import ReadOnlyViewset
from recipes.models import Tag, Ingredient, Recipe


class TagViewset(ReadOnlyViewset):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None
    
class IngredientViewset(ReadOnlyViewset):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngregientsSerializer
    pagination_class = None

class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    
    def perform_create(self, serializer):
        serializer.validated_data['author'] = serializer.context['request'].user
        return super().perform_create(serializer)