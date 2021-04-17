from django.contrib import admin
from .models import Recipe, RecipeEdition

admin.site.register([Recipe, RecipeEdition])