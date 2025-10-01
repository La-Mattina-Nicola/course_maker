from django.db import models
from django.conf import settings

class Famille(models.Model):
    nom = models.CharField(max_length=100)
    membres = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='familles')

    def __str__(self):
        return self.nom

class TypeIngredient(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(TypeIngredient, related_name="ingredients", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Unite(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class TypeRecette(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Recette(models.Model):
    name = models.CharField(max_length=300)
    type = models.ForeignKey(TypeRecette, related_name="recettes", on_delete=models.SET_NULL, null=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecetteIngredient', related_name="recettes")

    def __str__(self):
        return self.name

class RecetteIngredient(models.Model):
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unite = models.ForeignKey(Unite, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.quantity} {self.unite.name if self.unite else ''} de {self.ingredient.name} pour {self.recette.name}"

class ListeCourse(models.Model):
    famille = models.ForeignKey(Famille, related_name='listes_courses', on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} ({self.famille.nom})"

class ItemListeCourse(models.Model):
    liste = models.ForeignKey(ListeCourse, related_name='items', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantite = models.FloatField()
    unite = models.ForeignKey(Unite, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.quantite} {self.unite.name if self.unite else ''} de {self.ingredient.name}"
