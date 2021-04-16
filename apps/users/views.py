from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from .forms import UserRegistrationForm

class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    model = get_user_model()
    template_name = "users/register.html"
    success_url = "/"

class UserLoginView(LoginView):
    template_name = "users/login.html"

class UserLogoutView(LoginView):
    template_name = "users/logout.html"