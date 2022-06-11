from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from recipes import serializers
from recipes.viewsets import ReadOnlyViewset
from recipes.models import Tag, Ingredient, Recipe, Favorite, ShoppingCart
from users.models import User


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
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.RecipeGetSerializer
        else:
            return serializers.RecipeSerializer

    @action(['post', 'delete'], detail=True)
    def favorite(self, request, *args, **kwargs):
        id = kwargs['pk']
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipes=recipe).exists():
                return HttpResponseBadRequest(
                    'Рецепт уже в избранном!', status=400)
            favorite = Favorite.objects.get_or_create(user=user)[0]
            favorite.recipes.add(recipe)
            favorite.save()
            serializer = serializers.RecipeLiteSerializer(instance=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite = get_object_or_404(
                Favorite, user=user, recipes=recipe)
            favorite.recipes.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)