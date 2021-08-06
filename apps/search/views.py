from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from apps.ingredients.models import Ingredient, IngredientName
from apps.recipes.models import Recipe
from django.db.models import Q
from apps.search.forms import SearchForm


class SearchListView(FormMixin, ListView):
    model = Recipe
    template_name = "search/search.html"
    context_object_name = "recipes"
    paginate_by = 30
    form_class = SearchForm

    def get(self, request, *args, **kwargs):
        self.form = self.get_form(self.form_class)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            ingredient_restriction = self.form.cleaned_data \
                .get("ingredient_restriction")
            include_ingredient_names = self.form.cleaned_data \
                .get("include_ingredient_names").lower()
            exclude_ingredient_names = self.form.cleaned_data \
                .get("exclude_ingredient_names").lower()
            recipe_name = self.form.cleaned_data.get("recipe_name")

            restrict = "true" if ingredient_restriction else ""

            url_parameters = get_url_parameters(
                restrict=restrict,
                include=include_ingredient_names,
                exclude=exclude_ingredient_names,
                name=recipe_name
            )

            return redirect(reverse('search') + url_parameters)

        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        ingredient_restriction = self.request.GET.get("restrict", "")
        include_ingredient_names = self.request.GET.get("include", "")
        exclude_ingredient_names = self.request.GET.get("exclude", "")
        recipe_name = self.request.GET.get("name", "")

        url_parameters = get_url_parameters(
            restrict=ingredient_restriction,
            include=include_ingredient_names,
            exclude=exclude_ingredient_names,
            name=recipe_name
        )
        self.url_parameters = url_parameters
        if url_parameters == "":
            return []

        if include_ingredient_names:
            include_ingredient_names = include_ingredient_names.split(",")
        if exclude_ingredient_names:
            exclude_ingredient_names = exclude_ingredient_names.split(",")

        recipes = get_query_recipes(ingredient_restriction,
                                    include_ingredient_names,
                                    exclude_ingredient_names,
                                    recipe_name)

        return recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        if self.url_parameters == "":
            context["url_parameters"] = "?"
        else:
            context["url_parameters"] = self.url_parameters + "&"
        return context


def get_url_parameters(**kwargs):
    if all([value == "" for value in kwargs.values()]):
        return ""
    return "?" + "&".join([f"{kwarg}={value}"
                           for kwarg, value in kwargs.items()
                           if value != ""])


def get_query_recipes(ingredient_restriction,
                      include_ingredient_names,
                      exclude_ingredient_names,
                      recipe_name):

    include_ingredient_names_db = IngredientName.objects.filter(
        Q(singular__in=include_ingredient_names)
        | Q(plural__in=include_ingredient_names)
    )
    exclude_ingredient_names_db = IngredientName.objects.filter(
        Q(singular__in=exclude_ingredient_names)
        | Q(plural__in=exclude_ingredient_names)
    )
    recipes = Recipe.objects.all()

    if include_ingredient_names_db or ingredient_restriction:
        recipes = Recipe.objects.exclude(ingredients=None)

    if include_ingredient_names_db or exclude_ingredient_names_db:

        if not ingredient_restriction:
            ingredients = Ingredient.objects.filter(
                names__in=include_ingredient_names_db
            )
            for ingredient in ingredients:
                recipes = recipes.intersection(
                    Recipe.objects.filter(ingredients=ingredient)
                )

        if ingredient_restriction:
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

    if recipe_name:

        recipes = [recipe for recipe in recipes
                   if recipe_name.lower() in recipe.name.lower()]

    return recipes
