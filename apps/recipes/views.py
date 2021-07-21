from django.shortcuts import redirect
from django.views.generic import FormView, DetailView
from apps.recipes.models import Recipe
from apps.recipes.forms import SourceUrlForm
from apps.scraper.models import Source


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/view.html"
    context_object_name = "recipe"

    def get_object(self):
        recipe = Recipe.objects.filter(id=self.kwargs["recipe_id"])
        if not recipe:
            return redirect("/")
        this_recipe = recipe[0]
        return this_recipe


class InsertSourceFormView(FormView):
    form_class = SourceUrlForm
    template_name = "recipes/source.html"

    def form_valid(self, form):
        source_url = form.cleaned_data["source_url"]
        return redirect(f"/scraper/?source_url={source_url}")
