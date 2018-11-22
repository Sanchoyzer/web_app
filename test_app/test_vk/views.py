from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from . import vk_utils as vu


def index(request):
    return render(
        request,
        'index.html',
        context={
            'vk_oauth_url': vu.get_vk_oauth_url(request.build_absolute_uri(reverse('vk-login'))),
            'vk_message': None
        }
    )


def vk_login(request):
    code = request.GET.get('code', None)
    error = request.GET.get('error', None)
    error_description = request.GET.get('error_description', None)

    if code is not None:
        vk_oauth_url = None
        vk_message = 'Успешный вход'
        token = vu.get_vk_token(code, request.build_absolute_uri(reverse('vk-login')))
    else:
        vk_oauth_url = vu.get_vk_oauth_url(request.build_absolute_uri(reverse('vk-login')))
        vk_message = 'Ошибка: {}. {}'.format(error, error_description)

    return render(
        request,
        'index.html',
        context={
            'vk_oauth_url': vk_oauth_url,
            'vk_message': vk_message
        }
    )
