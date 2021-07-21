from django.db import models
from apps.users.models import User
from apps.ingredients.models import Ingredient


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(to=Ingredient,
                                         related_name="recipes")
    preparation_section = models.TextField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        return self.title


class IngredientLine(models.Model):
    text = models.CharField(max_length=255)
    recipe = models.ForeignKey(to=Recipe,
                               related_name="ingredient_lines",
                               on_delete=models.CASCADE,
                               null=True)

