from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView, View
from apps.ingredients.models import Ingredient, IngredientName
from apps.recipes.models import Recipe
from django.db.models import Q
from apps.search.forms import SearchByIngredientsForm, SearchByNameForm


class ExploreRecipesListView(ListView):
    model = Recipe
    template_name = "search/search.html"
    context_object_name = "recipes"

class SearchListView(ListView):
    model = Recipe
    template_name = "search/search.html"
    context_object_name = "recipes"
    queryset = []

    def post(self, request, *args, **kwargs):
        self.object_list = self.queryset
        context = self.get_context_data()
        if "search_mode" in request.POST:
            context["by_ingredients_form"] = SearchByIngredientsForm(request.POST)
        elif "recipe_name" in request.POST:
            context["by_name_form"] = SearchByNameForm(request.POST)
        return self.render_to_response(context, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["by_ingredients_form"] = SearchByIngredientsForm()
        context["by_name_form"] = SearchByNameForm()
        return context


class SearchByIngredientsView(FormView):
    http_method_names = ['post']
    form_class = SearchByIngredientsForm

    def form_valid(self, form):
        search_mode = form.cleaned_data.get("search_mode")
        include_ingredient_names = form.cleaned_data \
            .get("include_ingredient_names").strip(",").split(",")
        exclude_ingredient_names = form.cleaned_data \
            .get("exclude_ingredient_names").strip(",").split(",")

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

        return SearchListView.as_view(queryset=recipes)(self.request)

    def form_invalid(self, form):
        return SearchListView.as_view()(self.request)


class SearchByNameView(FormView):
    http_method_names = ['post']
    form_class = SearchByNameForm
    
    def form_valid(self, form):
        return redirect("/search")

    def form_invalid(self, form):
        return redirect("/search")
