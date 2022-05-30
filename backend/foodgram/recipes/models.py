from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    measurment_unit = models.CharField(max_length=10)


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    color = models.CharField(max_length=7) #TODO: Сделать валидация по регулярным выражениям для HEX
    slug = models.SlugField(unique=True)
    
    
class Recipe(models.Model):
    name = models.CharField(max_length=256)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes')
    text = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, related_name="recipes")
    tags = models.ManyToManyField(Tag, related_name='recipes')
    image = models.ImageField()
    cooking_time = models.IntegerField()