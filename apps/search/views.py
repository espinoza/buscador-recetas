from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView, View
from apps.ingredients.models import Ingredient, IngredientName
from apps.recipes.models import Recipe
from django.db.models import Q
from apps.search.forms import SearchButtonForm


class ExploreRecipesListView(ListView):
    model = Recipe
    template_name = "search/search.html"
    context_object_name = "recipes"

class SearchByIngredientView(ListView):
    model = Recipe
    template_name = "search/search.html"
    context_object_name = "recipes"

    def get_queryset(self, **kwargs):
        include_ingredient_names = self.request.GET.get("include", "") \
            .strip(",").split(",")
        exclude_ingredient_names = self.request.GET.get("exclude", "") \
            .strip(",").split(",")
        search_mode = self.request.GET.get("mode", "")

        include_ingredient_names_db = IngredientName.objects.filter(
            Q(singular__in=include_ingredient_names)
            | Q(plural__in=include_ingredient_names)
        )
        exclude_ingredient_names_db = IngredientName.objects.filter(
            Q(singular__in=exclude_ingredient_names)
            | Q(plural__in=exclude_ingredient_names)
        )
        recipes = Recipe.objects.exclude(ingredients=None)

        if include_ingredient_names_db or exclude_ingredient_names_db:

            if search_mode == "soft":
                ingredients = Ingredient.objects.filter(
                    names__in=include_ingredient_names_db
                )
                for ingredient in ingredients:
                    recipes = recipes.intersection(
                        Recipe.objects.filter(ingredients=ingredient)
                    )

            if search_mode == "hard":
                non_ingredients = Ingredient.objects.exclude(
                    names__in=include_ingredient_names_db
                )
                for ingredient in non_ingredients:
                    recipes = recipes.intersection(
                        Recipe.objects.exclude(ingredients=ingredient)
                    )

            ingredients_to_exclude = Ingredient.objects.filter(
                names__in=exclude_ingredient_names_db
            )
            for ingredient in ingredients_to_exclude:
                recipes = recipes.intersection(
                    Recipe.objects.exclude(ingredients=ingredient)
                )

        else:
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
        include_names = form.cleaned_data.get("include_ingredient_names")
        exclude_names = form.cleaned_data.get("exclude_ingredient_names")
        self.success_url = "/search/?mode=" + search_mode \
                           + "&include=" + include_names \
                           + "&exclude=" + exclude_names
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect("/search")


class SearchByNameButtonView(View):
    http_method_names = ['post']
    
    def post(self, request, *args, **kwargs):
        return redirect("/search")
