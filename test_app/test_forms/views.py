from django.views.generic import TemplateView, CreateView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views


class IndexView(TemplateView):
    template_name = 'test_forms/index.html'


class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html'


def logout_view(request):
    logout(request)
    return redirect('forms-index')


class SignUp(CreateView):
    template_name = 'registration/signup.html'



