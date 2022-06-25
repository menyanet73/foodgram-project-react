from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from users.serializers import RecipeLiteSerializer


class FavoriteShoplistModelMixin:
    def item_create(self, model, user, recipe):
        if model.objects.filter(user=user, recipes=recipe).exists():
            raise ValidationError(
                f'Recipe already in {model._meta.verbose_name}')
        item = model.objects.get_or_create(user=user)[0]
        item.recipes.add(recipe)
        serializer = RecipeLiteSerializer(instance=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def item_delete(self, model, user, recipe):
        if not model.objects.filter(user=user, recipes=recipe).exists():
            raise ValidationError(f'Recipe not in {model._meta.verbose_name}')
        item = model.objects.get(user=user, recipes=recipe)
        item.recipes.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)
