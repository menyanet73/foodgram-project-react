from rest_framework.exceptions import ValidationError

from users.serializers import RecipeLiteSerializer


class FavoriteModelMixin:
    def item_create(self, model, user, recipe):
        if model.objects.filter(user=user, recipes=recipe).exists():
            raise ValidationError(
                f'Recipe already in {model._meta.verbose_name}')
        item = model.objects.get_or_create(user=user)[0]
        item.recipes.add(recipe)
        serializer = RecipeLiteSerializer(instance=recipe)
        return serializer

    def item_delete(self, model, user, recipe):
        if not model.objects.filter(user=user, recipes=recipe).exists():
            raise ValidationError(f'Recipe not in {model._meta.verbose_name}')
        item = model.objects.get(user=user, recipes=recipe)
        item.recipes.remove(recipe)
