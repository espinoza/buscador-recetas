from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView
from apps.ingredients.models import Ingredient, IngredientName
from apps.recipes.models import Recipe
from django.db.models import Q
from apps.search.forms import SearchButtonForm


class SearchByIngredientView(ListView):
    model = Recipe
    template_name = "search/search.html"
    context_object_name = "recipes"

    def get_queryset(self, **kwargs):
        ingredient_names = self.request.GET.get("ingredients", "") \
                           .strip(",").split(",")
        search_mode = self.request.GET.get("mode", "")
        ingredient_names_db = IngredientName.objects.filter(
            Q(singular__in=ingredient_names) | Q(plural__in=ingredient_names)
        )

        if search_mode == "soft":
            recipes = Recipe.objects.exclude(ingredients=None)
            ingredients = Ingredient.objects.filter(
                names__in=ingredient_names_db
            )
            for ingredient in ingredients:
                recipes = recipes.intersection(
                    Recipe.objects.filter(ingredients=ingredient)
                )

        if search_mode == "hard":
            recipes = Recipe.objects.exclude(ingredients=None)
            non_ingredients = Ingredient.objects.exclude(
                names__in=ingredient_names_db
            )
            for ingredient in non_ingredients:
                recipes = recipes.intersection(
                    Recipe.objects.exclude(ingredients=ingredient)
                )

        if not ingredient_names_db:
            recipes = Recipe.objects.none()

        return recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["button_form"] = SearchButtonForm()
        return context
    
    
class SearchButtonView(FormView):
    http_method_names = ['post']
    form_class = SearchButtonForm

    def form_valid(self, form):
        search_mode = form.cleaned_data.get("search_mode")
        ingredient_names = form.cleaned_data.get("ingredient_names")
        self.success_url = "/search/?mode=" + search_mode \
                           + "&ingredients=" + ingredient_names
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect("/search")
