from django.urls import path
from . import views

urlpatterns = [

    path('new/source/',
         views.UpdateRecipeDatabase.as_view(),
         name='update_recipe_database'),

    path('get_sources',
         views.get_sources,
         name="get_sources"),

    path('get_recipes_from_sources',
         views.get_recipes_from_sources,
         name="get_recipes_from_sources"),

    path('',
         views.add_recipe_from_source),

]
