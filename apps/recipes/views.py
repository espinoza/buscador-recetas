from apps.recipes.models import Source, Host
from urllib.parse import urlparse
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.recipes.forms import SourceUrlForm
from apps.recipes.scraper import save_recipe_from_url


class UpdateRecipeDatabase(LoginRequiredMixin, FormView):
    """A view dedicated to different options to update the recipe
    database, including a form where a particular source can be inserted
    to get the recipe.
    """
    form_class = SourceUrlForm
    template_name = "recipes/source.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        source_url = form.cleaned_data["source_url"]
        return redirect(f"/recipes/?source_url={source_url}")


def add_recipe_from_source(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect("/")
    url = request.GET["source_url"]
    new_recipe = save_recipe_from_url(url)
    if not new_recipe:
        return redirect('update_recipe_database')
    return redirect('check_recipe_ingredients', recipe_id=new_recipe.id)


def go_to_source(request):
    """A view to find source in database, add 1 click to its click counter,
    and redirect to its url.
    """
    source_url = request.GET.get('source')
    source_parsed_url = urlparse(source_url)

    host = Host.objects.filter(
        url_scheme=source_parsed_url.scheme,
        url_netloc=source_parsed_url.netloc,
    )
    if not host:
        return redirect('source_not_found')

    path = source_parsed_url.path
    source = Source.objects.filter(host=host[0], url_path=path)
    if not source:
        return redirect('source_not_found')
    source = source[0]

    source.clicks += 1
    source.save()
    return redirect(source.url)
    

def source_not_found(request):
    """A view to say that a source is not found, when the user modify
    the 'source' url parameter.
    """
    return render(request, 'recipes/source_not_found.html')
