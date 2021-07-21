from django.shortcuts import redirect
from django.views.generic import FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.recipes.models import Recipe
from apps.recipes.forms import SourceUrlForm
from apps.scraper.models import Source


class InsertSourceFormView(LoginRequiredMixin, FormView):
    """A view dedicated to a form where source can be inserted to get
    the recipe.
    """
    form_class = SourceUrlForm
    template_name = "recipes/source.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.level != 1:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        source_url = form.cleaned_data["source_url"]
        return redirect(f"/scraper/?source_url={source_url}")
