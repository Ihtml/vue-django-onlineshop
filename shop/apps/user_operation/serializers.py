# _*_ coding: utf-8 _*_
__author__ = 'ife'
__date__ = '2019-01-29 23:36'

from rest_framework import serializers

from .models import UserFav


class UserFavSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFav
        fields = ("user", "goods")
