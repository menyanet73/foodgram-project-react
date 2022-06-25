from io import StringIO
from wsgiref.util import FileWrapper

from django.db.models import (Case, Exists, IntegerField, OuterRef, Q, Sum,
                              Value, When)
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet

from recipes import paginators, serializers
from recipes.filters import RecipeFilter
from recipes.mixins import FavoriteShoplistModelMixin
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from recipes.permissions import IsAuthorOrAuthOrReadOnly


class TagViewset(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None


class IngredientViewset(ReadOnlyModelViewSet):
    serializer_class = serializers.IngregientsSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get('name')
        if name:
            query_start = Q(name__istartswith=name.lower())
            query_contain = Q(name__icontains=name.lower())
            queryset = (queryset.filter(query_start | query_contain)
                        .annotate(search_type_ordering=Case(
                            When(query_start, then=Value(1)),
                            When(query_contain, then=Value(0)),
                            default=Value(-1),
                            output_field=IntegerField(),
                        ))).order_by('-search_type_ordering')
        return queryset


class RecipeViewset(FavoriteShoplistModelMixin, viewsets.ModelViewSet):
    pagination_class = paginators.PageNumberLimitPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    permission_classes = [IsAuthorOrAuthOrReadOnly, ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.GetRecipeSerializer
        return serializers.RecipeSerializer

    def get_queryset(self):
        favorites = Favorite.objects.filter(
            user=self.request.user.id,
            recipes=OuterRef('pk'))
        shopping_carts = ShoppingCart.objects.filter(
            user=self.request.user.id,
            recipes=OuterRef('pk'))
        queryset = Recipe.objects.annotate(
            is_favorited=Exists(favorites),
            is_in_shopping_cart=Exists(shopping_carts))
        return queryset.order_by('-created')

    def perform_create(self, serializer):
        serializer.validated_data[
            'author'] = serializer.context['request'].user
        return super().perform_create(serializer)

    @action(['post', 'delete'], detail=True)
    def favorite(self, request, pk, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return self.item_create(Favorite, request.user, recipe)
        if request.method == 'DELETE':
            return self.item_delete(Favorite, request.user, recipe)

    @action(['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return self.item_create(ShoppingCart, request.user, recipe)
        if request.method == 'DELETE':
            return self.item_delete(ShoppingCart, request.user, recipe)

    @action(['GET'], detail=False)
    def download_shopping_cart(self, request, *args, **kwargs):
        ingredients_amount = (IngredientAmount.objects
                              .filter(recipes__cart__user=request.user)
                              .values('ingredient__name',
                                      'ingredient__measurement_unit')
                              .annotate(sum_amount=Sum('amount')))
        shoplist = [ingredient for ingredient in ingredients_amount]
        content = 'Список продуктов от Foodgram: \n\n'
        for ingredient in shoplist:
            content += (f"{ingredient['ingredient__name']}, "
                        f"{ingredient['sum_amount']} "
                        f"{ingredient['ingredient__measurement_unit']}")
            if ingredient != shoplist[-1]:
                content += '\n'
        file = StringIO(content)
        response = HttpResponse(FileWrapper(file),
                                content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=shoplist.txt'
        return response
