from django.urls import path
from . import views

urlpatterns = [

    path(
        route='',
        view=views.SearchListView.as_view(),
        name='search'
    ),

]
