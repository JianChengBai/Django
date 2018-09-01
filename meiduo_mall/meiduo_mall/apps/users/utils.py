import re

from django.contrib.auth.backends import ModelBackend

from users.models import User


def jwt_response_payload_handler(tokon, user=None, request=None):

    """
    自定义jwt认证成功返回数据
    :param tokon:
    :param user:
    :param request:
    :return:
    """
    return {
        'token': tokon,
        'user_id': user.id,
        'username': user.username,
    }


def get_user_by_account(account):
    """
    根据账号获取user对象
    :param account: 账号，可以是用户名，也可以是手机号
    :return: User对象或者None
    """
    try:
        if re.match(r'1[3-9]\d{9}$', account):

            # 账号为手机号
            user = User.objects.get(mobile=account)

        else:

            # 账号为用户名
            user = User.objects.get(username=account)

    except User.DoesNotExist:
        return None

    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户名或手机号
    """
    def authenticate(self, request, username=None, password=None, **kwargs):

        user = get_user_by_account(username)

        if user is not None and user.check_password(password):

            return user









