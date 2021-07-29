from django.shortcuts import render, redirect
from django.template.defaulttags import register
from apps.recipes.models import Recipe
from apps.ingredients.models import Ingredient, IngredientName
from apps.ingredients.forms import CreateIngredientNameForm
from apps.ingredients.detect import detect_ingredients


def edit_ingredients(request):
    """A view to show a list of all ingredients with their different names,
    forms to add a new ingredient or ingredient name to an existing
    ingredient, and buttons to delete ingredients or ingredient names.
    """
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
    """A view for a post request to save an ingredient name, related to an
    existing ingredient or a new one.
    """
    if not request.user.is_staff:
        return redirect("/")

    if request.method == "POST":
        form = CreateIngredientNameForm(request.POST)
        if form.is_valid():
            new_ingredient_name = form.save(commit=False)
            ingredient_id = form.cleaned_data["ingredient_id"]
            if ingredient_id is None:
                ingredient = Ingredient.objects.create()
            else:
                ingredient = Ingredient.objects.get(id=ingredient_id)
            new_ingredient_name.ingredient = ingredient
            form.save()
            return redirect("edit_ingredients")

    return redirect("/")


def delete_ingredient(request, ingredient_id):
    """A view to delete an ingredient and its related ingredien names."""
    if not request.user.is_staff:
        return redirect("/")
    ingredient_to_delete = Ingredient.objects.get(id=ingredient_id)
    ingredient_to_delete.delete()
    return redirect('edit_ingredients')


def delete_ingredient_name(request, ingredient_name_id):
    """A view to delete an ingredient name, and the ingredient object
    if it results empty.
    """
    if not request.user.is_staff:
        return redirect("/")
    name_to_delete = IngredientName.objects.get(id=ingredient_name_id)
    ingredient = name_to_delete.ingredient
    name_to_delete.delete()
    if len(ingredient.names.all()) == 0:
        ingredient.delete()
    return redirect('edit_ingredients')


def detect_ingredients_for_all_recipes(request):
    """A view to go through each recipe and read ingredient lines to find
    ingredient names and then add relationship with the corresponing
    ingredient object.
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect("/")
    recipes = Recipe.objects.all()
    for recipe in recipes:
        detect_ingredients(recipe)
    return redirect("update_recipe_database")


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)