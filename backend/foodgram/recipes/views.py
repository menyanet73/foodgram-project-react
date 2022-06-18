from django.db.models import Sum
from django.http import HttpResponseBadRequest, FileResponse
from django.shortcuts import get_object_or_404
from requests import request
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes import paginators, serializers
from recipes.permissions import IsAuthor
from recipes.models import Favorite, Ingredient, IngredientAmount, Recipe, ShoppingCart, Tag
from recipes.viewsets import ReadOnlyViewset

class TagViewset(ReadOnlyViewset):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None


class IngredientViewset(ReadOnlyViewset):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngregientsSerializer
    pagination_class = None


class RecipeViewset(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeSerializer
    pagination_class = paginators.PageNumberLimitPagination
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            self.permission_classes = [IsAuthor,]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()
    
    def get_queryset(self):
        queryset = Recipe.objects.all()
        author = self.request.query_params.get('author')
        if self.request.query_params.get('is_favorite'):
            queryset = queryset.filter(favorites__user=self.request.user)
        if self.request.query_params.get('is_in_shopping_cart'):
            queryset = queryset.filter(cart__user=self.request.user)
        if author:
            queryset = queryset.filter(author__id=author)
        return queryset

    def perform_create(self, serializer):
        serializer.validated_data['author'] = serializer.context['request'].user
        return super().perform_create(serializer)

    @action(['post', 'delete'], detail=True)
    def favorite(self, request, pk, *args, **kwargs):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipes=recipe).exists():
                return HttpResponseBadRequest(
                    'Рецепт уже в избранном!', status=400)
            favorite = Favorite.objects.get(user=user)
            favorite.recipes.add(recipe)
            favorite.save()
            serializer = serializers.RecipeLiteSerializer(instance=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not Favorite.objects.filter(user=user, recipes=recipe).exists():
                return HttpResponseBadRequest(
                    'Такого рецепта нет в избранном!', status=400)
            favorite = Favorite.objects.get(user=user, recipes=recipe)
            favorite.recipes.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['post', 'delete'], detail=True)
    def shopping_cart(self, request, *args, **kwargs):
        id = kwargs['pk']
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=user, recipes=recipe).exists():
                return HttpResponseBadRequest(
                    'Рецепт уже в корзине!', status=400)
            shopping_cart = ShoppingCart.objects.get_or_create(user=user)[0]
            shopping_cart.recipes.add(recipe)
            shopping_cart.save()
            serializer = serializers.RecipeLiteSerializer(instance=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not ShoppingCart.objects.filter(user=user, recipes=recipe):
                return HttpResponseBadRequest(
                    'Такого рецепта нет в корзине!', status=400)
            shopping_cart = ShoppingCart.objects.get(user=user, recipes=recipe)
            shopping_cart.recipes.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['GET'], detail=False)
    def download_shopping_cart(self, request, *args, **kwargs):
        ingredients_amount = IngredientAmount.objects.filter(recipes__cart__user=request.user).values('id__name', 'id__measurement_unit').annotate(amount=Sum('amount'))
        shoplist = [ingredient for ingredient in ingredients_amount]
        content = ''
        for ingredient in shoplist:
            content += f"{ingredient['id__name']}, {ingredient['id__measurement_unit']} - {ingredient['amount']}"
            if ingredient != shoplist[-1]:
                content += '\n'
        response = FileResponse(content, content_type='text/plain')
        return response
