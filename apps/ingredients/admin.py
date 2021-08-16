from django.contrib import admin
from .models import Ingredient, IngredientName, UnknownIngredientName

admin.site.register([Ingredient, IngredientName, UnknownIngredientName])