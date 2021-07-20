from django.shortcuts import redirect
from django.views.generic import FormView, DetailView
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


class InsertSourceFormView(FormView):
    form_class = SourceUrlForm
    template_name = "recipes/source.html"

    def form_valid(self, form):
        source_url = form.cleaned_data["source_url"]
        return redirect(f"/scraper/?source_url={source_url}")
