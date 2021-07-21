from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from .forms import UserRegistrationForm
from .models import User


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    model = get_user_model()
    template_name = "users/register.html"
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(LoginView):
    template_name = "users/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)


class UserLogoutView(LogoutView):
    template_name = "users/logout.html"


class UserPasswordChangeView(PasswordChangeView):
    template_name = "users/password_change.html"
    success_url = "/users/edit/"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email',
              'birthday']
    template_name = "users/edit.html"

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        user = self.request.user
        return "/users/" + str(user.username) + "/profile"
