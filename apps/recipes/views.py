from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView, DetailView
from django.views.generic.edit import CreateView
from apps.recipes.models import Recipe, RecipeEdition, IngredientLine
from apps.recipes.forms import SourceUrlForm
from apps.scraper.models import Source
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
        context["page_title"] = "Nueva receta"
        context["number_of_ingredients"] = 1
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
        ingredient_lines = recipe_editions.last().ingredient_lines
        context["ingredient_lines"] = ingredient_lines
        context["number_of_ingredients"] = len(ingredient_lines.all())
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
        edition_id = self.kwargs.get("edition_id", None)
        if edition_id:
            edition = RecipeEdition.objects.filter(id=edition_id)
            if edition:
                return edition[0]
        recipe_editions = this_recipe.editions.all().order_by("created_at")
        return recipe_editions.last()


class RecipeHistoryListView(ListView):
    model = RecipeEdition
    template_name = "recipes/history.html"
    context_object_name = "editions"

    def get_queryset(self):
        recipe_id = self.kwargs["recipe_id"]
        recipe = Recipe.objects.filter(id=recipe_id)
        if not recipe:
            return redirect("/")
        this_recipe = recipe[0]
        return this_recipe.editions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_edition"] = self.get_queryset().last()
        return context


class InsertSourceFormView(FormView):
    form_class = SourceUrlForm
    template_name = "recipes/source.html"

    def form_valid(self, form):
        source_url = form.cleaned_data["source_url"]
        return redirect(f"/scraper/?source_url={source_url}")
