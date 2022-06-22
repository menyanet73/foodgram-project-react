from django.forms import ModelChoiceField
from django_filters import AllValuesMultipleFilter
from django_filters import rest_framework as filters
from users.models import User
from django_filters.rest_framework.filters import BooleanFilter

from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    tags = AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    is_favorited = BooleanFilter(field_name='is_favorited')
    is_in_shopping_cart = BooleanFilter(field_name='is_in_shopping_cart')
    author = ModelChoiceField(User.objects.all())

    class Meta:
        model = Recipe
        fields = ['tags', 'is_favorited',
                  'is_in_shopping_cart', 'author', ]
