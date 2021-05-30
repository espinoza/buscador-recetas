from django.urls import path
from . import views

urlpatterns = [

    path('do',
         views.SearchView.as_view(),
         name='do_search'),

    path('',
         views.SearchListView.as_view(),
         name='search'),

]
