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

    path('edit',
         views.edit_ingredients,
         name='edit_ingredients'),

    path('save_ingredient_name',
         views.save_ingredient_name,
         name='save_ingredient_name'),

    path('<int:ingredient_id>/delete',
         views.delete_ingredient,
         name='delete_ingredient'),

    path('name/<int:ingredient_name_id>/delete',
         views.delete_ingredient_name,
         name='delete_ingredient_name'),

]
