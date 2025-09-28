from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from .models import TypeIngredient, Ingredient, Recette
from .serializers import TypeIngredientSerializer, IngredientSerializer, RecetteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.

# return all

class TypeIngredientViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TypeIngredient.objects.all()
    serializer_class = TypeIngredientSerializer
    
class IngredientModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    
class RecetteViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Recette.objects.all()
    serializer_class = RecetteSerializer
    
    @action(
    detail=False,
    methods=["post"],
    permission_classes=[IsAuthenticated],
    )
    def createRecette(self, request, pk=None):
        try:
            name = request.data.get("name")
            idIngredient = request.data.get("ingredients")

            if not name or not idIngredient:
                return Response({"message": "donnée manquante"}, status=400)

            # idIngredient doit être une liste d'IDs
            ingredients = Ingredient.objects.filter(id__in=idIngredient)
            recette = Recette.objects.create(nom=name)
            recette.ingredients.set(ingredients)  # ✅ Utilisation correcte
            recette.save()

            return Response({"message": "Recette créée avec succès"}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
