from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='forms-index'),
    path('signup/', views.SignUp.as_view(), name='forms-signup'),
    path('login/', views.LoginView.as_view(), name='forms-login'),
    path('logout/', views.logout_view, name='forms-logout'),
]
