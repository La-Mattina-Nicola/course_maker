from rest_framework.serializers import ModelSerializer
from .models import TypeIngredient, Ingredient, Recette


class TypeIngredientSerializer(ModelSerializer):
    class Meta:
        model = TypeIngredient
        fields = "__all__"
        
class IngredientSerializer(ModelSerializer):
    type = TypeIngredientSerializer()
    class Meta:
        model = Ingredient
        fields = "__all__"
        
class RecetteSerializer(ModelSerializer):
    ingredients = IngredientSerializer(many = True)
    class Meta:
        model = Recette
        fields = "__all__"
        