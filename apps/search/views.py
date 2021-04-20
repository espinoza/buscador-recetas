from django.shortcuts import render
from django.views.generic import FormView
from apps.ingredients.models import Ingredient, IngredientName
from apps.recipes.models import Recipe
from django.db.models import Q


def search_by_ingredients(request):
    recipes = Recipe.objects.none()
    if request.method == "POST":
        ingredient_names = request.POST["ingredient_names"].split(",")
        ingredient_names.pop()
        saved_ingredient_names = IngredientName.objects.filter(
            Q(singular__in=ingredient_names) | Q(plural__in=ingredient_names)
        )
        ingredients = Ingredient.objects.filter(names__in=saved_ingredient_names)
        # recipes = Recipe.objects.filter(ingredients__ingredient_names__in=saved_ingredient_names)
        recipes = Recipe.objects.filter(ingredients__in=ingredients)
    return render(request, "search/search.html", {'recipes': recipes})
