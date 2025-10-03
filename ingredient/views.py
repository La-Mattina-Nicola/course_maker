from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.views import APIView
from .models import IngredientType, Ingredient, Recipe, Family, RecipeType, ShoppingList, ShoppingListItem
from rest_framework.permissions import AllowAny
from .serializers import (
    IngredientTypeSerializer, IngredientSerializer, RecipeSerializer,
    FamilySerializer, RecipeTypeSerializer, ShoppingListSerializer,
    ShoppingListItemSerializer, RegisterSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Utilisateur créé avec succès."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializer

class UserSearchView(APIView):
    permission_classes = [AllowAny]  # Ou IsAuthenticated si tu veux restreindre

    def get(self, request):
        username = request.query_params.get('username')
        email = request.query_params.get('email')
        user = None

        if username:
            user = User.objects.filter(username=username).first()
        elif email:
            user = User.objects.filter(email=email).first()

        if user:
            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_200_OK)
        return Response({"detail": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)

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

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Family, ShoppingList
from .serializers import FamilySerializer, ShoppingListSerializer

class UserDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        families = Family.objects.filter(members=user)
        family_data = FamilySerializer(families, many=True).data

        shopping_lists = ShoppingList.objects.filter(family__in=families)
        shopping_list_data = ShoppingListSerializer(shopping_lists, many=True).data

        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "families": family_data,
            "shopping_lists": shopping_list_data
        })
