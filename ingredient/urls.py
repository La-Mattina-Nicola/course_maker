from django.urls import path, include
from ingredient import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'typeingredients', views.TypeIngredientViewSet, "typeingredient")

router.register(r'ingredients', views.IngredientModelViewSet, "ingredient")

router.register(r'recettes', views.RecetteViewSet, "recette")


urlpatterns = [
    path("api/", include(router.urls)),
]
