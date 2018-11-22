from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import vk_utils as vu


def index(request):
    return render(
        request,
        'index.html',
        context={
            'vk_oauth_url': vu.get_vk_oauth_url(request.build_absolute_uri(reverse('vk-login'))),
            'vk_message': None,
            'vk_user': None,
            'vk_friends': None
        }
    )


def vk_login(request):
    code = request.GET.get('code', None)
    error = request.GET.get('error', None)
    error_description = request.GET.get('error_description', None)

    vk_oauth_url = None
    vk_message = None
    vk_user = None
    vk_friends = None

    if code is not None:
        token = vu.get_vk_token(code, request.build_absolute_uri(reverse('vk-login')))
        vk_user = vu.VkUserInfo.get_obj(token.get('user_id'), token.get('access_token'))

        friends_list = vu.VkUserInfo.get_user_friends(vk_user.id, 'random', 5)
        vk_friends = list(map(lambda friend_id: vu.VkUserInfo.get_obj(friend_id, token.get('access_token')), friends_list))
    elif error is not None:
        vk_oauth_url = vu.get_vk_oauth_url(request.build_absolute_uri(reverse('vk-login')))
        vk_message = 'Ошибка: {}. {}'.format(error, error_description)
    else:
        return HttpResponseRedirect(reverse('index'))

    return render(
        request,
        'index.html',
        context={
            'vk_oauth_url': vk_oauth_url,
            'vk_message': vk_message,
            'vk_user': vk_user,
            'vk_friends': vk_friends
        }
    )
