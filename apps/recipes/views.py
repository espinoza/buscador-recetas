from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import Recipe, RecipeEdition
from django.contrib.auth.mixins import LoginRequiredMixin


class RecipeEditionCreateView(LoginRequiredMixin, CreateView):
    model = RecipeEdition
    fields = ['title', 'ingredient_section', 'preparation_section']
    template_name = "recipes/edition.html"
    success_url = "/"


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
        return super().form_valid(form)


class EditRecipeView(RecipeEditionCreateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Editar receta"
        return context

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = user
        recipe = Recipe.objects.filter(id=self.kwargs['recipe_id'])
        if not recipe:
            return redirect("/")
        this_recipe = recipe[0]
        form.instance.recipe = this_recipe
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
            "ingredient_section": last_edition.ingredient_section,
            "preparation_section": last_edition.preparation_section
        }
        return initial_values
