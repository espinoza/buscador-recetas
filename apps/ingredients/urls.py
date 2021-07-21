from django.urls import path
from . import views

urlpatterns = [

    path('check_recipe/<int:recipe_id>',
         views.CheckRecipeIngredientsView.as_view(),
         name='check_recipe_ingredients'),

    path('add_new_to_recipe/<int:recipe_id>',
         views.AddNewIngredientView.as_view(),
         name='add_new_ingredient_to_recipe'),

]
