import random

from users.models import User
from . import constants
from celery_tasks.sms import tasks
from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from meiduo_mall.utils.exceptions import logger


class SMSCodeView(APIView):
    """发送短信验证码"""

    def get(self, request, mobile):

        # 1创建连接到redis的对象
        redis_conn = get_redis_connection('verify_codes')

        # 2,60秒内不允许重发短信
        send_flag = redis_conn.get('send_flag_%s' % mobile)

        if send_flag:

            return Response({"message": "发送短信过于频繁"}, status=status.HTTP_400_BAD_REQUEST)

        # 3.生成和发送短信验证码
        sms_code = '%06d' % random.randint(0, 999999)

        try:

            # 发送短信的异步任务必须通过delay调用
            tasks.send_sms_code.delay(mobile, sms_code, 5)

        except Exception as e:
            # 发送短信失败, 记录错误信息到日志中
            logger.error('发送短信失败！%s:%s' % (mobile, sms_code))
            return Response({"message": "发送短信失败!"}, status=status.HTTP_502_BAD_GATEWAY)

        # 4以下代码演示redis管道pipeline的使用
        pl = redis_conn.pipeline()
        pl.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, constants.SEND_SMS_TEMPLATE_ID)
        # 执行
        pl.execute()

        # 响应发送短信验证码结果
        return Response({"message": "OK"})
