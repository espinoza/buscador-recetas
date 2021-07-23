from django.contrib import admin
from .models import Recipe, IngredientLine, Host, Source

admin.site.register([Recipe, IngredientLine, Host, Source])