from django.shortcuts import redirect
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.recipes.forms import SourceUrlForm
from apps.recipes.scraper import save_recipe_from_url
from apps.recipes.source_finder import get_sources_for_all_hosts


class UpdateRecipeDatabase(LoginRequiredMixin, FormView):
    """A view dedicated to different options to update the recipe
    database, including a form where a particular source can be inserted
    to get the recipe.
    """
    form_class = SourceUrlForm
    template_name = "recipes/source.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.level != 1:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        source_url = form.cleaned_data["source_url"]
        return redirect(f"/recipes/?source_url={source_url}")


def add_recipe_from_source(request):
    if not request.user.is_authenticated or request.user.level != 1:
        return redirect("/")
    url = request.GET["source_url"]
    new_recipe = save_recipe_from_url(url)
    if not new_recipe:
        return redirect('update_recipe_database')
    return redirect('check_recipe_ingredients', recipe_id=new_recipe.id)


def get_sources(request):
    if not request.user.is_authenticated or request.user.level != 1:
        return redirect("/")
    get_sources_for_all_hosts()
    return redirect("update_recipe_database")