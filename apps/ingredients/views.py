from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.defaulttags import register
from apps.recipes.models import Recipe
from apps.ingredients.models import Ingredient, IngredientName
from apps.ingredients.forms import AddIngredientForm, CreateIngredientNameForm
from django.urls import reverse_lazy
from django.db.models import Q
import re


class CheckRecipeIngredientsView(LoginRequiredMixin, FormView):

    form_class = AddIngredientForm
    template_name = "ingredients/check-recipe.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect("/")
        recipe = Recipe.objects.filter(id=self.kwargs['recipe_id'])
        if not recipe:
            return redirect("/")
        self.recipe = recipe[0]
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        recipe = self.recipe
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
            create_ingredient_form = CreateIngredientNameForm(
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


def edit_ingredients(request):
    if not request.user.is_staff:
        return redirect("/")

    form = CreateIngredientNameForm()
    ingredients = Ingredient.objects.all()
    forms = {}
    for ingredient in ingredients:
        forms[ingredient] = CreateIngredientNameForm(
            auto_id="%s" + str(ingredient.id),
            initial={"ingredient_id": ingredient.id}
        )
    context = {
        "form": form,
        "forms": forms,
        "ingredients": ingredients,
    }

    return render(request, "ingredients/edit.html", context)


def save_ingredient_name(request):
    if not request.user.is_staff:
        return redirect("/")

    if request.method == "POST":
        form = CreateIngredientNameForm(request.POST)
        if form.is_valid():
            new_ingredient_name = form.save(commit=False)
            ingredient_id = form.cleaned_data["ingredient_id"]
            print(ingredient_id)
            if ingredient_id is None:
                ingredient = Ingredient.objects.create()
            else:
                ingredient = Ingredient.objects.get(id=ingredient_id)
            new_ingredient_name.ingredient = ingredient
            form.save()
            return redirect("edit_ingredients")

    return redirect("/")


def delete_ingredient(request, ingredient_id):
    if not request.user.is_staff:
        return redirect("/")
    ingredient_to_delete = Ingredient.objects.get(id=ingredient_id)
    ingredient_to_delete.delete()
    return redirect('edit_ingredients')


def delete_ingredient_name(request, ingredient_name_id):
    if not request.user.is_staff:
        return redirect("/")
    name_to_delete = IngredientName.objects.get(id=ingredient_name_id)
    ingredient = name_to_delete.ingredient
    name_to_delete.delete()
    if len(ingredient.names.all()) == 0:
        ingredient.delete()
    return redirect('edit_ingredients')


def detect_ingredients_for_all_recipes(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect("/")
    recipes = Recipe.objects.all()
    for recipe in recipes:
        detect_ingredients(recipe)
    return redirect("update_recipe_database")


def detect_ingredients(recipe):
    """Reads ingredient lines in a recipe to search for ingredient names
    and saves many to many relationship between the recipe and corresponding
    ingredient objects.
    """
    recipe.ingredients.clear()
    SPECIAL_CHARACTERS = ",.;:¡!¿?()/"

    for ingredient_line in recipe.ingredient_lines.all():
        line = ingredient_line.text.lower()

        # Ingredient line as a list of phrases without special characters
        for char in SPECIAL_CHARACTERS:
            line = line.replace(char, "&")
        phrases = [phrase.strip(" ") for phrase in re.split(r'&|\sy\s', line)
                                     if re.search(r'\w', phrase)]

        for phrase in phrases:
            # Analyse concatenations of words that could be ingredient names
            words = [word for word in phrase.split(" ")
                          if not word.isnumeric()]

            # The ingredient name is more likely to appear to the right
            for start in range(len(words)-1, -1, -1):
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
                        end = start
                    else:
                        end -= 1


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)