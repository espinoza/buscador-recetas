from django.urls import path
from . import views

urlpatterns = [

    path('new/',
         views.NewRecipeView.as_view(),
         name='new_recipe'),

    path('<int:recipe_id>/edit/',
         views.EditRecipeView.as_view(),
         name='recipe_edition'),

    path('<int:recipe_id>/',
         views.RecipeDetailView.as_view(),
         name='view_recipe'),

    path('<int:recipe_id>/history',
         views.RecipeHistoryListView.as_view(),
         name='recipe_history'),

    path('<int:recipe_id>/history/<int:edition_id>',
         views.RecipeDetailView.as_view(),
         name='recipe_history_item'),

    path('new/source/',
         views.InsertSourceFormView.as_view(),
         name='insert_source'),

]
