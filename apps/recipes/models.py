from django.db import models
from apps.users.models import User
from apps.ingredients.models import Ingredient


class Recipe(models.Model):
    author = models.ForeignKey(to=User, null=True,
                               on_delete=models.SET_NULL,
                               related_name="created_recipes")
    ingredients = models.ManyToManyField(to=Ingredient,
                                         related_name="recipes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RecipeEdition(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(to=User, null=True,
                               on_delete=models.SET_NULL,
                               related_name="recipe_editions")
    ingredient_section = models.TextField(max_length=5000)
    preparation_section = models.TextField(max_length=10000)
    recipe = models.ForeignKey(to=Recipe, related_name="editions",
                               on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class VideoURL(models.Model):
    url = models.CharField(max_length=255)
    recipe_edition = models.ForeignKey(to=RecipeEdition,
                                       related_name="video_urls",
                                       on_delete=models.CASCADE)
