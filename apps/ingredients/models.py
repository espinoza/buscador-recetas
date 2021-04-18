from django.db import models


class Ingredient(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class IngredientName(models.Model):
    name = models.CharField(max_length=255)
    ingredient = models.ForeignKey(to=Ingredient, related_name="names",
                                   on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
