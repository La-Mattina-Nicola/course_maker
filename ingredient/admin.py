from django.contrib import admin
from .models import TypeIngredient, Ingredient, Recette
# Register your models here.


admin.site.register(TypeIngredient)    
    
admin.site.register(Ingredient)

admin.site.register(Recette)