'''
1. вообще, для того, чтобы получать информацию о пользователе + его друзьях, не нужно делать oauth,
    ибо это все доступно по ключу приложения

2. можно было бы для работы с vk воспользоваться одноименной библиотекой (https://github.com/voronind/vk) ,
    но сделаем велосипед своими руками :)

3. Доки
    https://vk.com/dev/auth_sites
'''

import requests
import json


VK_API_VER = '5.87'
VK_API_URL_METHOD = 'https://api.vk.com/method/{}?{}&access_token={}&v={}'
VK_API_URL_OAUTH = 'https://oauth.vk.com/authorize?client_id={}&display={}&redirect_uri={}&scope={}&response_type={}&v={}'
VK_API_URL_GET_TOKEN = 'https://oauth.vk.com/access_token?client_id={}&client_secret={}&redirect_uri={}&code={}'

APP_ID = '6757102'
APP_KEY = 'kvUEvbuVEc5aSWLf4ldH'
SERVICE_KEY = '2dc114e72dc114e72dc114e7422da60e0922dc12dc114e7763278a25caea5969f628529'


class VkUserInfo:
    def __init__(self, id=None, first_name=None, last_name=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

    def get_username(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_user_link(self):
        if self.id is not None:
            return 'https://vk.com/id' + str(self.id)
        else:
            return None

    @staticmethod
    def get_vk_response(method_name, params, token):
        if token is None:
            token = SERVICE_KEY
        r = requests.get(VK_API_URL_METHOD.format(method_name, params, token, VK_API_VER))
        if r.status_code != requests.codes.ok:
            return None
        try:
            response_text = json.loads(r.text).get("response")
        except ValueError as ex:
            response_text = None
        return response_text

    @staticmethod
    def get_obj(user_id, token=None):
        if user_id is None:
            return None
        user_info = VkUserInfo.get_vk_response(f"users.get", f"user_ids={user_id}", token)
        if user_info is None or len(user_info) == 0:
            return None
        user_info_obj = VkUserInfo()
        user_info_obj.__dict__.update(user_info[0])
        return user_info_obj

    @staticmethod
    def get_user_friends(user_id, order, count, token=None):
        if user_id is None or order is None or not isinstance(count, int):
            return None
        user_friends = VkUserInfo.get_vk_response(f"friends.get", f"user_id={user_id}&order={order}&count={count}", token)
        if user_friends is None:
            return None
        return user_friends.get("items")


def get_vk_oauth_url(redirect_uri):
    return VK_API_URL_OAUTH.format(APP_ID, "popup", redirect_uri, "friends", "code", VK_API_VER)


def get_vk_token(code, redirect_uri):
    r = requests.get(VK_API_URL_GET_TOKEN.format(APP_ID, APP_KEY, redirect_uri, code))
    if r.status_code != requests.codes.ok:
        return None
    return json.loads(r.text)
