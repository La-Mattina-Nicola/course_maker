from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from .models import TypeIngredient, Ingredient, Recette
from .serializers import TypeIngredientSerializer, IngredientSerializer, RecetteSerializer
from rest_framework.permissions import IsAuthenticated

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