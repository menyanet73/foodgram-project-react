from django.contrib import admin
from recipes import models

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'amount')
    
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')

# TODO: Настроить админку

admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.IngredientAmount, IngredientAmountAdmin)