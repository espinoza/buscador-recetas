from django.contrib import admin
from .models import Ingredient, IngredientName

admin.site.register([Ingredient, IngredientName])