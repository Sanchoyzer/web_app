from django.views.generic import TemplateView, ListView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.urls import reverse

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm


class IndexView(TemplateView):
    template_name = 'test_forms/index.html'


class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html'


def logout_view(request):
    logout(request)
    return redirect('forms-index')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user_obj = form.cleaned_data
            username = user_obj['username']
            password = user_obj['password']
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, password=password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('forms-index')
            else:
                return render(request, 'registration/error.html',
                              {'error_msg': 'Такой пользователь уже существует', 'prev_url': reverse('forms-index')})
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})


class UsersView(ListView):
    model = User
    context_object_name = 'users'
    queryset = User.objects.filter(is_active=True).order_by('username')
    template_name = 'test_forms/users.html'

