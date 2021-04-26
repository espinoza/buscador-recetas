from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView, DetailView
from django.views.generic.edit import CreateView
from apps.recipes.models import Recipe, RecipeEdition, IngredientLine
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/explore.html"
    context_object_name = "recipes"


class RecipeEditionCreateView(LoginRequiredMixin, CreateView):
    model = RecipeEdition
    fields = ['title', 'preparation_section']
    template_name = "recipes/edition.html"

    def get_success_url(self, **kwargs):
        recipe_id = self.object.recipe.id
        return reverse_lazy('check_recipe_ingredients',
                            kwargs={"recipe_id": recipe_id})

class NewRecipeView(RecipeEditionCreateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Nueva receta"
        return context

    def form_valid(self, form):

        user = self.request.user
        form.instance.author = user
        new_recipe = Recipe.objects.create(author=user)
        form.instance.recipe = new_recipe
        form.save()

        number_of_ingredients = self.request.POST["number_of_ingredients"]
        saved_ingredients = 0
        ingredient_number = 1
        while saved_ingredients < int(number_of_ingredients):
            ingredient_line = self.request.POST \
                .get("ingredient_line_" + str(ingredient_number), None)
            if ingredient_line:
                new_ingredient_line = IngredientLine.objects.create(
                    text=ingredient_line
                )
                form.instance.ingredient_lines.add(new_ingredient_line)
                saved_ingredients += 1
            ingredient_number += 1

        return super().form_valid(form)


class EditRecipeView(RecipeEditionCreateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Editar receta"
        recipe = Recipe.objects.filter(id=self.kwargs['recipe_id'])
        if not recipe:
            return redirect("/")
        this_recipe = recipe[0]
        recipe_editions = this_recipe.editions.all().order_by("created_at")
        context["ingredient_lines"] = recipe_editions.last().ingredient_lines
        return context

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = user
        recipe = Recipe.objects.filter(id=self.kwargs['recipe_id'])
        if not recipe:
            return redirect("/")
        this_recipe = recipe[0]
        form.instance.recipe = this_recipe
        form.save()

        number_of_ingredients = self.request.POST["number_of_ingredients"]
        saved_ingredients = 0
        ingredient_number = 1
        while saved_ingredients < int(number_of_ingredients):
            ingredient_line = self.request.POST \
                .get("ingredient_line_" + str(ingredient_number), None)
            if ingredient_line:
                new_ingredient_line = IngredientLine.objects.create(
                    text=ingredient_line
                )
                form.instance.ingredient_lines.add(new_ingredient_line)
                saved_ingredients += 1
            ingredient_number += 1

        return super().form_valid(form)

    def get_initial(self):
        recipe = Recipe.objects.filter(id=self.kwargs['recipe_id'])
        if not recipe:
            return redirect("/")
        this_recipe = recipe[0]
        recipe_editions = this_recipe.editions.all().order_by("created_at")
        last_edition = recipe_editions.last()
        initial_values = {
            "title": last_edition.title,
            "preparation_section": last_edition.preparation_section
        }
        return initial_values


class RecipeDetailView(DetailView):
    model = RecipeEdition
    template_name = "recipes/view.html"
    context_object_name = "edition"

    def get_object(self):
        recipe = Recipe.objects.filter(id=self.kwargs["recipe_id"])
        if not recipe:
            return redirect("/")
        this_recipe = recipe[0]
        recipe_editions = this_recipe.editions.all().order_by("created_at")
        last_edition = recipe_editions.last()
        return last_edition
