from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import (
    IngredientType, Ingredient, Recipe, RecipeIngredient,
    Unit, Family, RecipeType, ShoppingList, ShoppingListItem
)
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer, CharField, ValidationError


class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True)
    password2 = CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError({"password": "Les mots de passe ne correspondent pas."})
        validate_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
    
class IngredientTypeSerializer(ModelSerializer):
    class Meta:
        model = IngredientType
        fields = "__all__"

class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'type']

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

class IngredientTypeSerializer(ModelSerializer):
    class Meta:
        model = IngredientType
        fields = "__all__"

class IngredientSerializer(ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=IngredientType.objects.all())
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'type']

class RecipeIngredientCreateSerializer(ModelSerializer):
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']

class RecipeCreateSerializer(ModelSerializer):
    ingredients = RecipeIngredientCreateSerializer(many=True)
    type = serializers.PrimaryKeyRelatedField(queryset=RecipeType.objects.all())

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'type', 'ingredients']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for item in ingredients_data:
            RecipeIngredient.objects.create(recipe=recipe, **item)
        return recipe
