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


# 不用modelserializer的原因是：VerifyCode中code是必填字段，这里只用验证手机号
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


class UserSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4)

    def validate_code(self, code):
        # 在ModelSerializer中, self.initial_data为用户前端传进来的值, 这里username等价于mobile
        verify_recodes = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by("add_time")
        if verify_recodes:
            last_records = verify_recodes[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago < last_records.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_records.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    class Meta:
        model = User
        # 这里的User用的是userProfile 继承的是Django自带的User username是必填字段
        fileds = ("username", "code", "mobile")
