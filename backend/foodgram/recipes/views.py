import io
from uuid import uuid4
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from django.core.files.base import ContentFile
from django.http import HttpResponseBadRequest, HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from wsgiref.util import FileWrapper

from foodgram.settings import MEDIA_ROOT
from recipes import paginators, serializers
from recipes.models import Favorite, Ingredient, IngredientAmount, Recipe, ShoppingCart, Tag
from recipes.viewsets import ReadOnlyViewset
from recipes.instruments import create_pdf


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
    
    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_favorite = self.request.query_params.get('is_favorite')
        in_shopping_cart = self.request.query_params.get('is_in_shopping_cart')
        author = self.request.query_params.get('author')
        if is_favorite:
            queryset = queryset.filter(favorites__user=self.request.user)
        if in_shopping_cart:
            queryset = queryset.filter(cart__user=self.request.user)
        if author:
            queryset = queryset.filter(author__id=author)
        return queryset

    def perform_create(self, serializer):
        serializer.validated_data['author'] = serializer.context['request'].user
        return super().perform_create(serializer)

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
            if not Favorite.objects.filter(user=user, recipes=recipe):
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
        ingredients_amount = IngredientAmount.objects.filter(recipes__cart__user=request.user).prefetch_related('id')
        ingredients = [ingredient.id.name for ingredient in ingredients_amount]
        measurement_units = [ingredient.id.measurement_unit for ingredient in ingredients_amount]
        amount = [ingredient.amount for ingredient in ingredients_amount]
        shoplist = zip(ingredients, amount, measurement_units)
        shopdict = {}
        for ingredient in shoplist:
            if f'{ingredient[0]}, {ingredient[2]}' in shopdict:
                shopdict[f'{ingredient[0]}, {ingredient[2]}'] += ingredient[1]
            else:
                shopdict[f'{ingredient[0]}, {ingredient[2]}'] = ingredient[1]
        # name = f'{MEDIA_ROOT}/recipes/shoplists/{request.user.username}_shoplist.pdf'
        shoplist_string = ''
        shoplist_string = [f'{ingredient} - {shopdict[ingredient]}' for ingredient in shopdict]
        buffer = io.BytesIO()
        content = '\n'.join(shoplist_string)
        # create_pdf(buffer, content)
        # response = HttpResponse(FileWrapper(buffer), content_type='application/pdf')
        response = FileResponse(content, content_type='text/plain')
        return response
