from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from . import vk_utils as vu


COOKIE_MESSAGE = 'message'
COOKIE_TOKEN = 'token'
COOKIE_USER = 'user_id'


def index(request):
    vk_message = request.session.get(COOKIE_MESSAGE, None)
    token = request.session.get(COOKIE_TOKEN, None)
    vk_user = None
    vk_friends = None
    if token is not None:
        vk_user = vu.VkUserInfo.get_obj(request.session.get(COOKIE_USER, None), token)
        if vk_user is not None:
            friends_list = vu.VkUserInfo.get_user_friends(vk_user.id, 'random', 5)
            vk_friends = list(map(lambda friend_id: vu.VkUserInfo.get_obj(friend_id, token), friends_list))

    return render(
        request,
        'index.html',
        context={
            'vk_oauth_url': vu.get_vk_oauth_url(request.build_absolute_uri(reverse('vk-login'))),
            'vk_message': vk_message,
            'vk_user': vk_user,
            'vk_friends': vk_friends
        }
    )


def vk_login(request):
    code = request.GET.get('code', None)
    error = request.GET.get('error', None)
    error_description = request.GET.get('error_description', None)

    if code is not None:
        token = vu.get_vk_token(code, request.build_absolute_uri(reverse('vk-login')))
        user_id = token.get(COOKIE_USER)
        if user_id is None:
            request.session[COOKIE_MESSAGE] = '{}: {}'.format(token.get('error'), token.get('error_description'))
        else:
            # не заморачиваемся безопасностью и проверкой через set_test_cookie :)
            request.session[COOKIE_USER] = user_id
            request.session[COOKIE_TOKEN] = token.get('access_token')
            request.session.set_expiry(token.get('expires_in', 0))
    elif error is not None:
        request.session[COOKIE_MESSAGE] = '{}: {}'.format(error, error_description)
    return HttpResponseRedirect(reverse('index'))
