from django.urls import path
from . import views

urlpatterns = [

    path('',
         views.SearchByIngredientView.as_view(),
         name='search_by_ingredients'),

    path('do',
         views.SearchButtonView.as_view(),
         name="do_search_by_ingredients"),

    path('do_name',
         views.SearchByNameButtonView.as_view(),
         name='do_search_by_name'),

    path('explore',
         views.ExploreRecipesListView.as_view(),
         name='explore'),

]
