from django.urls import path
from . import views

urlpatterns = [

    path('by_ingredients',
         views.SearchByIngredientsView.as_view(),
         name="search_by_ingredients"),

    path('by_name',
         views.SearchByNameView.as_view(),
         name='search_by_name'),

    path('explore',
         views.ExploreRecipesListView.as_view(),
         name='explore'),

    path('',
         views.SearchListView.as_view(),
         name='search'),

]
