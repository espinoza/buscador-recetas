from django.urls import path
from . import views

urlpatterns = [

    path('new/source/',
         views.UpdateRecipeDatabase.as_view(),
         name='update_recipe_database'),

    path('get_sources',
         views.get_sources,
         name="get_sources"),

    path('',
         views.add_recipe_from_source),

]
