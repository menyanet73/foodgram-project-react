from django.db import models
from django.core.validators import MinValueValidator

from users.models import User
from recipes.validators import validate_color


class Ingredient(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=10, verbose_name='Ед. измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}'


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount', verbose_name='Ингредиент')
    amount = models.IntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиента'

    def __str__(self) -> str:
        return f'{self.id.name} {self.amount}'


class Tag(models.Model):
    name = models.CharField(
        max_length=30, unique=True, verbose_name='Название')
    color = models.CharField(
        max_length=7, validators=[validate_color], verbose_name='Цвет')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор')
    text = models.TextField(verbose_name='Текст')
    ingredients = models.ManyToManyField(
        IngredientAmount, related_name="recipes", verbose_name='Ингредиенты')
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Теги')
    image = models.ImageField(verbose_name='Изображение')
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(1)]
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['id']

    def __str__(self) -> str:
        return self.name

    def in_favorites(self):
        return Favorite.objects.filter(recipes__id__exact=self.id).count()


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipes = models.ManyToManyField(
        Recipe, related_name='favorites', verbose_name='Рецепты')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    recipes = models.ManyToManyField(
        Recipe, related_name='cart', verbose_name='Рецепты')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
