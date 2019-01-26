# _*_ coding: utf-8 _*_
__author__ = 'ife'
__date__ = '2019-01-24 22:36'

import re
from datetime import datetime, timedelta
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

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


class UserRegSerializer(serializers.ModelSerializer):
    # code验证码是多余字段， 不会保存到数据库中
    # write_only设置为 True 可确保在更新或创建实例时可以使用该字段，但在序列化表示时不包括该字段
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4,label='验证码', help_text='验证码',
                                 error_messages={
                                    "blank": "验证码不能为空",
                                    "required": "请输入验证码",
                                    "max_length": "验证码格式错误",
                                    "min_length": "验证码格式错误"
                                 })

    username = serializers.CharField(label='用户名', help_text='用户名', required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已存在')])

    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    # 修改密码，之前是明文
    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        # 在ModelSerializer中, self.initial_data为用户前端传进来的值, 这里username等价于mobile
        verify_recodes = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by("-add_time")
        if verify_recodes:
            last_records = verify_recodes[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_records.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_records.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        # 不需要前端传mobile，后端设置
        attrs["mobile"] = attrs["username"]
        # user model里并没有code字段, 所以删掉
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        # 这里的User用的是userProfile 继承的是Django自带的User username是必填字段
        fields = ("username", "code", "mobile", "password")
