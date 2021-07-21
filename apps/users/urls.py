from django.urls import path
from . import views

urlpatterns = [

    path('login/',
         views.UserLoginView.as_view(),
         name='login'),

    path('logout/',
         views.UserLogoutView.as_view(),
         name='logout'),

    path('password_change/',
         views.UserPasswordChangeView.as_view(),
         name='password_change'),

    path('registration/',
         views.UserRegistrationView.as_view(),
         name='registration'),

    path('edit/',
         views.UserUpdateView.as_view(),
         name='edit_user'),

]
