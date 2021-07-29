from django.urls import path
from . import views

urlpatterns = [

    path(
        route='new/source/',
        view=views.UpdateRecipeDatabase.as_view(),
        name='update_recipe_database'
    ),

    path(
        route='get_sources',
        view=views.get_sources,
        name="get_sources"
    ),

    path(
        route='get_recipes_from_sources',
        view=views.get_recipes_from_sources,
        name="get_recipes_from_sources"
    ),

    path(
        route='',
        view=views.add_recipe_from_source
    ),

]
