from django.contrib import admin
from .models import (
    Family, Ingredient, ShoppingListItem, ShoppingList,
    RecipeIngredient, Recipe, IngredientType, RecipeType, Unit
)

admin.site.register(Family)
admin.site.register(Ingredient)
admin.site.register(ShoppingListItem)
admin.site.register(ShoppingList)
admin.site.register(RecipeIngredient)
admin.site.register(Recipe)
admin.site.register(IngredientType)
admin.site.register(RecipeType)
admin.site.register(Unit)
