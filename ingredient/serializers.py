from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import (
    IngredientType, Ingredient, Recipe, RecipeIngredient,
    Unit, Family, RecipeType, ShoppingList, ShoppingListItem
)

class IngredientTypeSerializer(ModelSerializer):
    class Meta:
        model = IngredientType
        fields = "__all__"

class IngredientSerializer(ModelSerializer):
    type = IngredientTypeSerializer()
    class Meta:
        model = Ingredient
        fields = "__all__"

class RecipeTypeSerializer(ModelSerializer):
    class Meta:
        model = RecipeType
        fields = "__all__"

class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"

class RecipeIngredientSerializer(ModelSerializer):
    ingredient = IngredientSerializer()
    unit = UnitSerializer()
    class Meta:
        model = RecipeIngredient
        fields = "__all__"

class RecipeSerializer(ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, source='recipeingredient_set')
    type = RecipeTypeSerializer()
    class Meta:
        model = Recipe
        fields = "__all__"

class FamilySerializer(ModelSerializer):
    member_names = SerializerMethodField()

    class Meta:
        model = Family
        fields = ['id', 'name', 'member_names']

    def get_member_names(self, obj):
        return [user.get_full_name() or user.username for user in obj.members.all()]

class ShoppingListSerializer(ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = "__all__"

class ShoppingListItemSerializer(ModelSerializer):
    ingredient_name = SerializerMethodField()
    unit_name = SerializerMethodField()

    class Meta:
        model = ShoppingListItem
        fields = ['id', 'list', 'quantity', 'ingredient', 'ingredient_name', 'unit', 'unit_name']

    def get_ingredient_name(self, obj):
        return obj.ingredient.name if obj.ingredient else None

    def get_unit_name(self, obj):
        return obj.unit.name if obj.unit else None
