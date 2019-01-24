# _*_ coding: utf-8 _*_
__author__ = 'ife'
__date__ = '2019-01-24 22:36'

import re
from datetime import datetime, timedelta
from rest_framework import serializers
from django.contrib.auth import get_user_model

from shop.settings import REGEX_MOBILE
from .models import VerifyCode


User = get_user_model()


# 不用modelserializer的原因是：VerifyCode中code是必填字段，这里只用到手机号
class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """
        # 验证手机号是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("请填写正确的手机号码")

        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上次发送未超过60s")

        return mobile
