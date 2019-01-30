# _*_ coding: utf-8 _*_
__author__ = 'ife'
__date__ = '2019-01-29 23:36'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav


class UserFavSerializer(serializers.ModelSerializer):
    # 获取到当前的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]
        # 要做删除功能需要把ID传过去
        fields = ("user", "goods", "id")
