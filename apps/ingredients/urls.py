from django.urls import path
from . import views

urlpatterns = [

    path(
        route='edit',
        view=views.edit_ingredients,
        name='edit_ingredients'
    ),

    path(
        route='save_ingredient_name',
        view=views.save_ingredient_name,
        name='save_ingredient_name'
    ),

    path(
        route='<int:ingredient_id>/delete',
        view=views.delete_ingredient,
        name='delete_ingredient'
    ),

    path(
        route='name/<int:ingredient_name_id>/delete',
        view=views.delete_ingredient_name,
        name='delete_ingredient_name'
    ),

]
