from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView
from apps.recipes.models import Recipe
from apps.ingredients.models import Ingredient, IngredientName
from apps.ingredients.forms import AddIngredientForm, CreateIngredientForm
from django.urls import reverse_lazy
from django.db.models import Q
import re


class CheckRecipeIngredientsView(FormView):

    form_class = AddIngredientForm
    template_name = "ingredients/check_recipe.html"

    def get_context_data(self, **kwargs):
        recipe = Recipe.objects.filter(id=self.kwargs['recipe_id'])
        if not recipe:
            return redirect("/")
        this_recipe = recipe[0]
        recipe_editions = this_recipe.editions.all().order_by("created_at")
        last_edition = recipe_editions.last()
        detect_ingredients(this_recipe, last_edition)
        context = super().get_context_data(**kwargs)
        context["ingredients"] = this_recipe.ingredients
        context["ingredient_lines"] = last_edition.ingredient_lines.all()
        context["recipe_id"] = this_recipe.id
        context["recipe_title"] = last_edition.title
        return context

    def form_valid(self, form):
        recipe = Recipe.objects.filter(id=self.kwargs['recipe_id'])
        if not recipe:
            return redirect("/")
        this_recipe = recipe[0]

        recipe_editions = this_recipe.editions.all().order_by("created_at")
        last_edition = recipe_editions.last()
        new_ingredient_on_recipe = form.cleaned_data.get("new_ingredient")
        if not any(new_ingredient_on_recipe in ingredient_line.text
                   for ingredient_line in last_edition.ingredient_lines.all()):
            return redirect("/")

        names_found = IngredientName.objects.filter(
            Q(singular=new_ingredient_on_recipe)
            | Q(plural=new_ingredient_on_recipe)
        )
        if names_found:
            this_recipe.ingredients.add(names_found[0].ingredient)
        else:
            create_ingredient_form = CreateIngredientForm()
            return self.render_to_response(
                self.get_context_data(
                    create_ingredient_form=create_ingredient_form)
            )

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        recipe_id = self.kwargs['recipe_id']
        return reverse_lazy('check_recipe_ingredients',
                            kwargs={"recipe_id": recipe_id})


class AddNewIngredientToRecipeView(CreateView):
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


def detect_ingredients(recipe, recipe_edition):
    if recipe_edition.recipe is not recipe:
        return None
    special_characters = ",.;:¡!¿?()/"
    for ingredient_line in recipe_edition.ingredient_lines.all():
        line = ingredient_line.text
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
