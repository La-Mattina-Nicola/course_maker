from django.db import models
from django.conf import settings

class Family(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='families')

    def __str__(self):
        return self.name

class IngredientType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(IngredientType, related_name="ingredients", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class RecipeType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(RecipeType, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name="recipes")

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.quantity} {self.unit.name if self.unit else ''} of {self.ingredient.name} for {self.recipe.name}"

class ShoppingList(models.Model):
    family = models.ForeignKey(Family, related_name='shopping_lists', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.family.name})"

class ShoppingListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, null=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.quantity} {self.unit.name if self.unit else ''} of {self.ingredient.name}"
