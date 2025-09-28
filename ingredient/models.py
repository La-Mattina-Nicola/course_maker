from django.db import models

# Create your models here.

class TypeIngredient(models.Model):
    name = models.CharField()
    
    def __str__(self):
        return self.name
    
class Ingredient(models.Model):
    name = models.CharField()
    type = models.ForeignKey(TypeIngredient, related_name="ingredient", on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name
    
class Recette(models.Model):
    name = models.CharField()
    ingredients = models.ManyToManyField(Ingredient, related_name="recettes")
    def __str__(self):
        return self.name
    