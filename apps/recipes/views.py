from django.shortcuts import redirect
from django.views.generic import FormView, ListView, DetailView
from apps.recipes.models import Recipe, RecipeEdition
from apps.recipes.forms import SourceUrlForm
from apps.scraper.models import Source


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
