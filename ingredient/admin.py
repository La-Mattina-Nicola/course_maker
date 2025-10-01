from django.contrib import admin
from .models import Famille, Ingredient, ItemListeCourse, ListeCourse, RecetteIngredient, Recette, TypeIngredient, TypeRecette, Unite
# Register your models here.


admin.site.register(Famille)
admin.site.register(Ingredient)
admin.site.register(ItemListeCourse)
admin.site.register(ListeCourse)
admin.site.register(RecetteIngredient)
admin.site.register(Recette)
admin.site.register(TypeIngredient)
admin.site.register(TypeRecette)
admin.site.register(Unite)

