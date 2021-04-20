from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_by_ingredients, name='search_by_ingredients')
]
