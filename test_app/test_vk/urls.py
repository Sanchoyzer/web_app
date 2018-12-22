from django.urls import path

from . import views

urlpatterns = [    
    path('', views.index, name='vk-index'),
    path('vk_login', views.vk_login, name='vk-login'),
]
