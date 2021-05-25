from django.urls import path
from . import views

urlpatterns = [

    path('do',
         views.SearchView.as_view(),
         name='do_search'),

    path('explore',
         views.ExploreRecipesListView.as_view(),
         name='explore'),

    path('',
         views.SearchListView.as_view(),
         name='search'),

]
