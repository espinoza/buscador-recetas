from django.urls import path
from . import views

urlpatterns = [

    path('login/',
         views.UserLoginView.as_view(),
         name='login'),

    path('logout/',
         views.UserLogoutView.as_view(),
         name='logout'),

    path('registration/',
         views.UserRegistrationView.as_view(),
         name='registration'),

    path('<str:username>/profile/',
         views.ProfileDetailView.as_view(),
         name='profile'),

    path('edit/',
         views.UserUpdateView.as_view(),
         name='edit_user'),

]
