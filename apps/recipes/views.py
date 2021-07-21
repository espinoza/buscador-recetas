from django.shortcuts import redirect
from django.views.generic import FormView, DetailView
from apps.recipes.models import Recipe
from apps.recipes.forms import SourceUrlForm
from apps.scraper.models import Source


class InsertSourceFormView(FormView):
    form_class = SourceUrlForm
    template_name = "recipes/source.html"

    def form_valid(self, form):
        source_url = form.cleaned_data["source_url"]
        return redirect(f"/scraper/?source_url={source_url}")
