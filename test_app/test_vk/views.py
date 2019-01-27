from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import vk_utils as vku

COOKIE_MESSAGE = 'message'
COOKIE_TOKEN = 'token'
COOKIE_USER = 'user_id'


def index(request):
    vk_message = request.session.get(COOKIE_MESSAGE)
    token = request.session.get(COOKIE_TOKEN)
    vk_user = None
    if token is not None:
        vk_user = vku.VkUserInfo.get_obj(request.session.get(COOKIE_USER), token)
    vk_friends = None
    if vk_user is not None:
        friends_list = vku.VkUserInfo.get_user_friends(vk_user.id, 'random', 5, token)
        if friends_list is not None:
            vk_friends = [vku.VkUserInfo.get_obj(friend_id, token) for friend_id in friends_list]

    return render(
        request,
        'test_vk/index.html',
        context={
            'vk_oauth_url': vku.get_vk_oauth_url(request.build_absolute_uri(reverse('vk-login'))),
            'vk_message': vk_message,
            'vk_user': vk_user,
            'vk_friends': vk_friends
        }
    )


def vk_login(request):
    code = request.GET.get('code')
    error = request.GET.get('error')
    error_description = request.GET.get('error_description')

    if code is not None:
        token = vku.get_vk_token(code, request.build_absolute_uri(reverse('vk-login')))
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
    return HttpResponseRedirect(reverse('vk-index'))
