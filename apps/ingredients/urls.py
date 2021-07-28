from django.urls import path
from . import views

urlpatterns = [

    path('check_recipe/<int:recipe_id>',
         views.CheckRecipeIngredientsView.as_view(),
         name='check_recipe_ingredients'),

    path('detect_ingredients_for_all_recipes',
         views.detect_ingredients_for_all_recipes,
         name='detect_ingredients_for_all_recipes'
    ),

    path('add_new_to_recipe/<int:recipe_id>',
         views.AddNewIngredientView.as_view(),
         name='add_new_ingredient_to_recipe'),

]
