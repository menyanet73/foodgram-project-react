from django.contrib import admin

from recipes import models


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_id', 'amount')
    list_filter = ('id__name',)
    list_select_related = ('id',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'cooking_time', 'in_favorites')
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('in_favorites', )

    def in_favorites(self, obj):
        return obj.in_favorites()


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user',)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.IngredientAmount, IngredientAmountAdmin)
admin.site.register(models.Favorite, FavoriteAdmin)
admin.site.register(models.ShoppingCart, ShoppingCartAdmin)
