from django.shortcuts import redirect
from django.views.generic import FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.recipes.models import Recipe
from apps.ingredients.models import Ingredient, IngredientName
from apps.ingredients.forms import AddIngredientForm, CreateIngredientForm
from django.urls import reverse_lazy
from django.db.models import Q
import re


class CheckRecipeIngredientsView(LoginRequiredMixin, FormView):

    form_class = AddIngredientForm
    template_name = "ingredients/check-recipe.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.level != 1:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        recipe = Recipe.objects.filter(id=self.kwargs['recipe_id'])
        if not recipe:
            return redirect("/")
        recipe = recipe[0]
        detect_ingredients(recipe)
        context = super().get_context_data(**kwargs)
        context.update({
            "ingredients": recipe.ingredients,
            "ingredient_lines": recipe.ingredient_lines.all(),
            "recipe_id": recipe.id,
            "recipe_title": recipe.title,
        })
        return context

    def form_valid(self, form):
        recipe = Recipe.objects.filter(id=self.kwargs['recipe_id'])
        if not recipe:
            return redirect("/")
        recipe = recipe[0]

        new_ingredient_on_recipe = form.cleaned_data.get("new_ingredient")
        if not any(new_ingredient_on_recipe in ingredient_line.text
                   for ingredient_line in recipe.ingredient_lines.all()):
            return redirect("/")

        names_found = IngredientName.objects.filter(
            Q(singular=new_ingredient_on_recipe)
            | Q(plural=new_ingredient_on_recipe)
        )
        if names_found:
            recipe.ingredients.add(names_found[0].ingredient)
        else:
            create_ingredient_form = CreateIngredientForm(
                initial={
                    "singular": new_ingredient_on_recipe.lower(),
                    "plural": new_ingredient_on_recipe.lower(),
                }
            )
            return self.render_to_response(
                self.get_context_data(
                    create_ingredient_form=create_ingredient_form)
            )

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        recipe_id = self.kwargs['recipe_id']
        return reverse_lazy('check_recipe_ingredients',
                            kwargs={"recipe_id": recipe_id})


class AddNewIngredientView(LoginRequiredMixin, CreateView):
    """A view to recive a post request to add a new ingredient when it
    is not detected in any ingredient line of the recipe.
    """
    http_method_names = ['post']
    model = IngredientName
    fields = ['singular', 'plural']

    def form_valid(self, form):
        new_ingredient_name = form.save(commit=False)
        new_ingredient = Ingredient.objects.create()
        new_ingredient_name.ingredient = new_ingredient
        form.save()
        recipe_id = self.kwargs["recipe_id"]
        recipe = Recipe.objects.filter(id=recipe_id)
        if recipe:
            recipe[0].ingredients.add(new_ingredient)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        recipe_id = self.kwargs['recipe_id']
        return reverse_lazy('check_recipe_ingredients',
                            kwargs={"recipe_id": recipe_id})


def detect_ingredients(recipe):
    special_characters = ",.;:¡!¿?()/"
    for ingredient_line in recipe.ingredient_lines.all():
        line = ingredient_line.text.lower()
        for char in special_characters:
            line.replace(char, "&")
        phrases = re.split(r'[&]', line)
        for phrase in phrases:
            words = phrase.split(" ")
            for start in range(len(words)):
                end = len(words)
                ingredient_found = False
                while not ingredient_found and end > start:
                    mini_phrase = " ".join(words[start:end])
                    ingredients = Ingredient.objects.filter(
                        Q(names__singular=mini_phrase)
                        | Q(names__plural=mini_phrase)
                    )
                    if ingredients:
                        ingredient_found = True
                        recipe.ingredients.add(*ingredients)
                    end -= 1
