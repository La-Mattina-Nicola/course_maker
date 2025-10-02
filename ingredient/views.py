from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import IngredientType, Ingredient, Recipe, Family, RecipeType, ShoppingList, ShoppingListItem

from .serializers import (
    IngredientTypeSerializer, IngredientSerializer, RecipeSerializer,
    FamilySerializer, RecipeTypeSerializer, ShoppingListSerializer,
    ShoppingListItemSerializer
)

class ShoppingListViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ShoppingList.objects.all().order_by('id')
    serializer_class = ShoppingListSerializer

class ShoppingListItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ShoppingListItem.objects.all().order_by('id')
    serializer_class = ShoppingListItemSerializer

class FamilyViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Family.objects.all().order_by('id')
    serializer_class = FamilySerializer

class RecipeTypeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = RecipeType.objects.all().order_by('id')
    serializer_class = RecipeTypeSerializer

class IngredientTypeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = IngredientType.objects.all().order_by('id')
    serializer_class = IngredientTypeSerializer

class IngredientViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Ingredient.objects.all().order_by('id')
    serializer_class = IngredientSerializer

class RecipeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Recipe.objects.all().order_by('id')
    serializer_class = RecipeSerializer

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def create_recipe(self, request):
        try:
            name = request.data.get("name")
            ingredient_ids = request.data.get("ingredients")

            if not name or not ingredient_ids:
                return Response({"message": "Missing data"}, status=400)

            ingredients = Ingredient.objects.filter(id__in=ingredient_ids)
            recipe = Recipe.objects.create(name=name)
            recipe.ingredients.set(ingredients)

            return Response({"message": "Recipe created successfully"}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
