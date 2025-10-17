from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import (
    IngredientType, Ingredient, Recipe, Family, RecipeType,
    ShoppingList, ShoppingListItem, Unit
)
from .serializers import (
    IngredientTypeSerializer, IngredientSerializer, RecipeSerializer,
    FamilySerializer, RecipeTypeSerializer, ShoppingListSerializer,
    ShoppingListItemSerializer, RegisterSerializer, UnitSerializer, RecipeCreateSerializer
)

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

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        })

    def put(self, request):
        user = request.user
        username = request.data.get('username')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')

        if username:
            # Vérifie que le username n'existe pas déjà
            if User.objects.filter(username=username).exclude(id=user.id).exists():
                return Response({"detail": "Ce username est déjà utilisé."}, status=400)
            user.username = username
        if email:
            user.email = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if password:
            validate_password(password)
            user.set_password(password)

        user.save()
        return Response({"detail": "Profil mis à jour avec succès."})

class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]

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

    @action(detail=False, methods=['post'], url_path='add-recipe')
    def add_recipe(self, request):
        recipe_id = request.data.get('recipe_id')
        shopping_list_id = request.data.get('shopping_list_id')
        user = request.user

        # Récupère la famille de l'utilisateur
        family = Family.objects.filter(members=user).first()
        if not family:
            return Response({"detail": "Aucune famille trouvée."}, status=400)

        # Récupère la shopping list par ID
        try:
            shopping_list = ShoppingList.objects.get(id=shopping_list_id, family=family)
        except ShoppingList.DoesNotExist:
            return Response({"detail": "Liste de course introuvable ou non autorisée."}, status=404)

        # Récupère la recette
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return Response({"detail": "Recette introuvable."}, status=404)

        # Ajoute chaque ingrédient de la recette à la shopping list
        for ri in recipe.recipeingredient_set.all():
            ShoppingListItem.objects.create(
                shopping_list=shopping_list,
                ingredient=ri.ingredient,
                quantity=ri.quantity,
                unit=ri.unit
            )

        return Response({"detail": f"Recette ajoutée à la liste '{shopping_list.name}' de la famille."})

    @action(detail=True, methods=['delete'], url_path='clear-items')
    def clear_items(self, request, pk=None):
        shopping_list = self.get_object()
        deleted_count, _ = ShoppingListItem.objects.filter(shopping_list=shopping_list).delete()
        return Response(
            {"detail": f"{deleted_count} items supprimés de la liste."},
            status=status.HTTP_200_OK
        )

class ShoppingListItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ShoppingListItem.objects.all().order_by('id')
    serializer_class = ShoppingListItemSerializer

    def get_queryset(self):
        user = self.request.user
        families = Family.objects.filter(members=user)
        shopping_lists = ShoppingList.objects.filter(family__in=families)
        return ShoppingListItem.objects.filter(shopping_list__in=shopping_lists).order_by('id')

class FamilyViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Family.objects.all().order_by('id')
    serializer_class = FamilySerializer

    def perform_create(self, serializer):
        family = serializer.save()
        family.members.add(self.request.user)
        ShoppingList.objects.create(family=family)

    @action(detail=True, methods=['post'], url_path='add-members')
    def add_members(self, request, pk=None):
        family = self.get_object()
        user_ids = request.data.get('user_ids', [])
        if not isinstance(user_ids, list):
            return Response({"detail": "user_ids doit être une liste d'identifiants utilisateur."}, status=400)
        users = User.objects.filter(id__in=user_ids)
        for user in users:
            family.members.add(user)
        return Response({"detail": f"{users.count()} membres ajoutés à la famille."})
    
    @action(detail=True, methods=['post'], url_path='remove-members')
    def remove_members(self, request, pk=None):
        family = self.get_object()
        user_ids = request.data.get('user_ids', [])
        if not isinstance(user_ids, list):
            return Response({"detail": "user_ids doit être une liste d'identifiants utilisateur."}, status=400)
        users = User.objects.filter(id__in=user_ids)
        for user in users:
            family.members.remove(user)
        return Response({"detail": f"{users.count()} membres retirés de la famille."})

    @action(detail=True, methods=['post'], url_path='add-favorite')
    def add_favorite(self, request, pk=None):
        family = self.get_object()
        recipe_id = request.data.get('recipe_id')
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return Response({"detail": "Recette introuvable."}, status=404)
        family.favorite_recipes.add(recipe)
        return Response({"detail": "Recette ajoutée aux favoris."})

    @action(detail=True, methods=['post'], url_path='remove-favorite')
    def remove_favorite(self, request, pk=None):
        family = self.get_object()
        recipe_id = request.data.get('recipe_id')
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return Response({"detail": "Recette introuvable."}, status=404)
        family.favorite_recipes.remove(recipe)
        return Response({"detail": "Recette retirée des favoris."})

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
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['type']  

class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']          
    filterset_fields = ['type']        

    def get_serializer_class(self):
        if self.action == 'create':
            return RecipeCreateSerializer
        return RecipeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        read_serializer = RecipeSerializer(recipe)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

class UserDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        families = Family.objects.filter(members=user)
        family_data = FamilySerializer(families, many=True).data

        shopping_lists = ShoppingList.objects.filter(family__in=families)
        shopping_lists_response = []
        for shopping_list in shopping_lists:
            items = ShoppingListItem.objects.filter(shopping_list=shopping_list)
            items_data = [
                {
                    "id": item.id,
                    "ingredient_name": item.ingredient.name if item.ingredient else None,
                    "ingredient_type": item.ingredient.type.name if item.ingredient and item.ingredient.type else None,
                    "quantity": item.quantity,
                    "unit": item.unit.name if item.unit else None
                }
                for item in items
            ]
            shopping_lists_response.append({
                "id": shopping_list.id,
                "name": shopping_list.name,
                "created_at": shopping_list.created_at,
                "family": shopping_list.family.id,
                "items": items_data
            })

        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            "families": family_data,
            "shopping_lists": shopping_lists_response
        })

class UnitViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Unit.objects.all().order_by('id')
    serializer_class = UnitSerializer
