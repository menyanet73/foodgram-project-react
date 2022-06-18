from django.urls import include, path
from rest_framework import routers
from recipes import views


router = routers.SimpleRouter()
router.register(r'tags', views.TagViewset)
router.register(r'ingredients', views.IngredientViewset)
router.register(r'recipes', views.RecipeViewset, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
]
