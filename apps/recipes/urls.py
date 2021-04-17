from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.NewRecipeView.as_view(), name='new_recipe'),
    path('<int:recipe_id>/edit/', views.EditRecipeView.as_view(), name='recipe_edition'),
]
