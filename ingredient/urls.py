from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IngredientTypeViewSet, IngredientViewSet, RecipeTypeViewSet, RecipeViewSet, FamilyViewSet, ShoppingListViewSet, ShoppingListItemViewSet


router = DefaultRouter()
router.register(r'ingredient-types', IngredientTypeViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipe-types', RecipeTypeViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'families', FamilyViewSet)
router.register(r'shopping-lists', ShoppingListViewSet)
router.register(r'shopping-list-items', ShoppingListItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
