from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from .forms import UserRegistrationForm
from .models import User

class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    model = get_user_model()
    template_name = "users/register.html"
    success_url = "/"

class UserLoginView(LoginView):
    template_name = "users/login.html"

class UserLogoutView(LogoutView):
    template_name = "users/logout.html"


class ProfileDetailView(DetailView):
    model = User
    template_name = "users/profile.html"
    context_object_name = "user"

    def get_object(self):
        username = self.kwargs["username"]
        user = User.objects.filter(username=username)
        if not user:
            return redirect("/")
        profile_user = user[0]
        return profile_user