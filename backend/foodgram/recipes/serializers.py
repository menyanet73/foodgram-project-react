from base64 import b64decode
from rest_framework import serializers
from recipes.models import IngredientAmount, Tag, Ingredient, Recipe
from PIL import Image



class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Tag
        
        
class IngregientsSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Ingredient
        

class IngredientAmountSerializer(serializers.ModelSerializer):
    # id = serializers.SerializerMethodField()
    
    class Meta:
        fields = ['id', 'amount']
        model = IngredientAmount

    # def get_id(self, obj):
    #     return obj.ingredient
        
        
class ImageSerializerField(serializers.Field):
    def to_internal_value(self, data):
        image = b64decode(data)
        name = 'newimagename'
        save_image = open(name, 'wb').write(image)
        save_image.close()
        
        return super().to_internal_value(data)
    

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountSerializer(many=True)
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    
    class Meta:
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorite',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        ]
        read_only_fields = ['author']
        model = Recipe
        
    def get_is_favorite(self, obj):
        return None

    def get_is_in_shopping_cart(self, obj):
        return None
    
    def to_internal_value(self, data):
        return super().to_internal_value(data)