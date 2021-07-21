from django.views.generic import ListView, FormView
from apps.ingredients.models import Ingredient, IngredientName
from apps.recipes.models import Recipe
from django.db.models import Q
from apps.search.forms import SearchForm


class SearchListView(ListView):
    model = Recipe
    template_name = "search/search.html"
    context_object_name = "recipes"
    queryset = []

    def post(self, request, *args, **kwargs):
        self.object_list = self.queryset
        context = self.get_context_data()
        context["form"] = SearchForm(request.POST)
        return self.render_to_response(context, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm()
        return context


class SearchView(FormView):
    http_method_names = ['post']
    form_class = SearchForm

    def form_valid(self, form):
        ingredient_restriction = form.cleaned_data \
            .get("ingredient_restriction")
        include_ingredient_names = form.cleaned_data \
            .get("include_ingredient_names").strip(",").split(",")
        exclude_ingredient_names = form.cleaned_data \
            .get("exclude_ingredient_names").strip(",").split(",")
        recipe_name = form.cleaned_data.get("recipe_name")

        recipes = get_query_recipes(ingredient_restriction,
                                    include_ingredient_names,
                                    exclude_ingredient_names,
                                    recipe_name)

        return SearchListView.as_view(queryset=recipes)(self.request)

    def form_invalid(self, form):
        return SearchListView.as_view()(self.request)


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
