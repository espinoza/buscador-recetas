from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from apps.ingredients.models import (
    Ingredient, IngredientName, UnknownIngredientName
)
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

        # 'unknown_ingredient_names' should exist only if this get method
        # is executed due to a redirect from post method
        request.session["post_step"] = request.session.get("post_step", 0) + 1
        if request.session["post_step"] > 1:
            request.session["unknown_ingredient_names"] = None

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

            # Unknown (or inactive known) ingredients are not used
            known_included, unknown_included = split_known_unknown(
                include_ingredient_names
            )
            known_excluded, unknown_excluded = split_known_unknown(
                exclude_ingredient_names
            )

            # Unknown (or inactive known) ingredients are reported
            unknown_names = set(unknown_included + unknown_excluded)
            for name in unknown_names:
                UnknownIngredientName.objects.get_or_create(name=name)

            url_parameters_str = get_url_parameters_str(
                restrict=restrict,
                include=",".join(known_included),
                exclude=",".join(known_excluded),
                name=recipe_name
            )

            # Unknown (or inactive known) ingredients are shown in template
            request.session["unknown_names"] = ", ".join(set(unknown_names))
            request.session["post_step"] = 0

            return redirect(reverse('search') + url_parameters_str)

        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        ingredient_restriction = self.request.GET.get("restrict", "")
        include_ingredient_names = self.request.GET.get("include", "")
        exclude_ingredient_names = self.request.GET.get("exclude", "")
        recipe_name = self.request.GET.get("name", "")

        url_parameters = {
            "restrict": ingredient_restriction,
            "include": include_ingredient_names,
            "exclude": exclude_ingredient_names,
            "name": recipe_name
        }
        self.url_parameters = url_parameters

        if all([value == "" for value in url_parameters.values()]):
            return []

        if include_ingredient_names:
            include_ingredient_names = include_ingredient_names.split(",")
        if exclude_ingredient_names:
            exclude_ingredient_names = exclude_ingredient_names.split(",")

        recipes = get_query_recipes(
            ingredient_restriction=ingredient_restriction,
            include_ingredient_names=include_ingredient_names,
            exclude_ingredient_names=exclude_ingredient_names,
            recipe_name=recipe_name
        )

        return recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = self.form
        form.initial = {
            "ingredient_restriction": self.url_parameters["restrict"],
            "include_ingredient_names": self.url_parameters["include"],
            "exclude_ingredient_names": self.url_parameters["exclude"],
            "recipe_name": self.url_parameters["name"]
        }
        context["form"] = form

        url_parameters_str = get_url_parameters_str(**self.url_parameters)
        if url_parameters_str == "":
            context["url_parameters"] = "?"
        else:
            context["url_parameters"] = url_parameters_str + "&"
        return context


def get_url_parameters_str(**kwargs):
    """Return a string containing url parameters just as they should appear
    at url.  The input is passed as one keyword argument for each parameter.
    """
    if all([value == "" for value in kwargs.values()]):
        return ""
    return "?" + "&".join([f"{kwarg}={value}"
                           for kwarg, value in kwargs.items()
                           if value != ""])


def split_known_unknown(ingredient_names_str):
    """Get a string with comma separated ingredient names and return two
    lists: known ingredient names and unknown ingredient names.
    """
    if ingredient_names_str == "":
        return [], []

    ingredient_names_list = ingredient_names_str.split(",")
    known_ingredient_names = []
    unknown_ingredient_names = []

    for name in ingredient_names_list:
        # If an ingredient name exists but is not active, it is reported
        # to the user as unknown to avoid confusion about exixting ingredient
        # names that are not in search results
        cleaned_name = " ".join(name.strip().split(" "))
        names_found = IngredientName.objects.filter(
            Q(singular=cleaned_name, is_active=True)
            | Q(plural=cleaned_name, is_active=True)
        )
        if names_found and cleaned_name not in known_ingredient_names:
            known_ingredient_names.append(cleaned_name)
        elif name not in unknown_ingredient_names:
            unknown_ingredient_names.append(cleaned_name)

    return known_ingredient_names, unknown_ingredient_names


def get_query_recipes(ingredient_restriction,
                      include_ingredient_names,
                      exclude_ingredient_names,
                      recipe_name):

    include_ingredient_names_db = IngredientName.objects.filter(
        Q(singular__in=include_ingredient_names, is_active=True)
        | Q(plural__in=include_ingredient_names, is_active=True)
    )
    exclude_ingredient_names_db = IngredientName.objects.filter(
        Q(singular__in=exclude_ingredient_names, is_active=True)
        | Q(plural__in=exclude_ingredient_names, is_active=True)
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
