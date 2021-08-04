from django.urls import path
from . import views

urlpatterns = [

    path(
        route='new/source/',
        view=views.UpdateRecipeDatabase.as_view(),
        name='update_recipe_database'
    ),

    path(
        route='',
        view=views.add_recipe_from_source
    ),

]
