from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView
from apps.recipes.models import Recipe
from apps.ingredients.models import Ingredient, IngredientName
from apps.ingredients.forms import AddIngredientForm, CreateIngredientForm
from django.urls import reverse_lazy
from django.db.models import Q


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
        if new_ingredient_on_recipe not in last_edition.ingredient_section:
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

