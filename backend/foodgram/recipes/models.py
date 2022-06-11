from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    measurement_unit = models.CharField(max_length=10)
    
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        
    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}'
        

class IngredientAmount(models.Model):
    item_id = models.AutoField(primary_key=True)
    id = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='amount')
    amount = models.IntegerField()
    
    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиента'
        
    def __str__(self) -> str:
        return f'{self.id.name} {self.amount}'


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    color = models.CharField(max_length=7) #TODO: Сделать валидация по регулярным выражениям для HEX
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        
    def __str__(self) -> str:
        return self.name
    
    
class Recipe(models.Model):
    name = models.CharField(max_length=256)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes')
    text = models.TextField()
    ingredients = models.ManyToManyField(
        IngredientAmount, related_name="recipes")
    tags = models.ManyToManyField(Tag, related_name='recipes')
    image = models.ImageField()
    cooking_time = models.IntegerField()
    
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        
    def __str__(self) -> str:
        return self.name