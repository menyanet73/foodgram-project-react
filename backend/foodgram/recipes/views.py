import os

from django.db.models import (Case, Exists, IntegerField, OuterRef, Q, Sum,
                              Value, When)
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from foodgram.settings import STATIC_ROOT
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import exceptions
from users.serializers import RecipeLiteSerializer

from recipes import paginators, serializers
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from recipes.filters import RecipeFilter
from recipes.permissions import IsAuthor
from recipes.viewsets import ReadOnlyViewset


class TagViewset(ReadOnlyViewset):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None


class IngredientViewset(ReadOnlyViewset):
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


class RecipeViewset(viewsets.ModelViewSet):
    pagination_class = paginators.PageNumberLimitPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.GetRecipeSerializer
        return serializers.RecipeSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            self.permission_classes = [IsAuthor, ]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

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
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipes=recipe).exists():
                raise exceptions.ValidationError('Recipe already in favorites')
            favorite = Favorite.objects.create(user=user)
            favorite.recipes.add(recipe)
            favorite.save()
            serializer = RecipeLiteSerializer(instance=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not Favorite.objects.filter(user=user, recipes=recipe).exists():
                raise exceptions.ValidationError('Recipe not in favorites')
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
                raise exceptions.ValidationError('Recipe already in shopcart')
            shopping_cart = ShoppingCart.objects.get_or_create(user=user)[0]
            shopping_cart.recipes.add(recipe)
            shopping_cart.save()
            serializer = RecipeLiteSerializer(instance=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not ShoppingCart.objects.filter(user=user, recipes=recipe):
                raise exceptions.ValidationError('Recipe not in shopcart')
            shopping_cart = ShoppingCart.objects.get(user=user, recipes=recipe)
            shopping_cart.recipes.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['GET'], detail=False)
    def download_shopping_cart(self, request, *args, **kwargs):
        ingredients_amount = (IngredientAmount.objects
                              .filter(recipes__cart__user=request.user)
                              .values('id__name', 'id__measurement_unit')
                              .annotate(amount=Sum('amount')))
        shoplist = [ingredient for ingredient in ingredients_amount]
        content = ''
        for ingredient in shoplist:
            content += (f"{ingredient['id__name']}, "
                        f"{ingredient['amount']} "
                        f"{ingredient['id__measurement_unit']}")
            if ingredient != shoplist[-1]:
                content += '\n'
        path = os.path.join(STATIC_ROOT, 'shoplist.txt')
        temp = open(path, 'w')
        temp.write(content)
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=shoplist.txt'
        response.write(content)
        return response
