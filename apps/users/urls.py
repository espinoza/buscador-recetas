from django.urls import path
from . import views

urlpatterns = [

    path(
        route='login/',
        view= views.UserLoginView.as_view(),
        name='login'
    ),

    path(
        route='logout/',
        view=views.UserLogoutView.as_view(),
        name='logout'
    ),

    path(
        route='password_change/',
        view=views.UserPasswordChangeView.as_view(),
        name='password_change'
    ),

    path(
        route='registration/',
        view=views.UserRegistrationView.as_view(),
        name='registration'
    ),

    path(
        route='edit/',
        view=views.UserUpdateView.as_view(),
        name='edit_user'
    ),

]
