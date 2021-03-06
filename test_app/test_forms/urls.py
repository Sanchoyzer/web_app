from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='forms-index'),
    path('signup/', views.register, name='forms-signup'),
    path('login/', views.LoginView.as_view(), name='forms-login'),
    path('logout/', views.logout_view, name='forms-logout'),
    path('users/', views.UsersView.as_view(), name='forms-users'),
    path('send_email_log/', views.EmailLogView.as_view(), name='forms-email-log'),
    path('feedback/', views.feedback, name='forms-feedback'),
]
