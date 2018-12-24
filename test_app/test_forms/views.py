from django.views.generic import TemplateView, ListView
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import get_connection, send_mail, mail_admins, send_mass_mail

from smtplib import SMTPException
from threading import Thread

from .forms import UserRegistrationForm
from .models import EmailLog

from dotenv import dotenv_values as dtv


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


def send_email_background():
    connection = get_connection(
        host=dtv().get('EMAIL_HOST'),
        port=dtv().get('EMAIL_PORT'),
        username=dtv().get('EMAIL_HOST_USER'),
        password=dtv().get('EMAIL_HOST_PASSWORD'),
        use_tls=bool(int(dtv().get('EMAIL_USE_SSL', '1')))
    )

    superusers_emails_queryset = User.objects.filter(is_superuser=True, email__isnull=False).values_list('email')
    superusers_emails = list(email_item[0] for email_item in superusers_emails_queryset)
    try:
        num_sent = send_mail(
            subject='Тема письма',
            message='Тело',
            from_email=dtv().get('EMAIL_HOST_USER'),
            recipient_list=superusers_emails,
            connection=connection
        )
    except SMTPException:
        num_sent = 0

    log = EmailLog()
    log.is_success = (num_sent > 0)
    log.save()


def send_email(request):
    t = Thread(target=send_email_background, args=())
    t.start()
    return redirect('forms-index')


class EmailLogView(ListView):
    model = EmailLog
    context_object_name = 'logs'
    queryset = EmailLog.objects.all().order_by('date')
    template_name = 'test_forms/log.html'

