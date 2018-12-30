# _*_ coding: utf-8 _*_
__author__ = 'ife'
__date__ = '2018-12-30 18:33'

from rest_framework import serializers


class GoodsSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=100)
    # drf的serializers会自动把文件路径转换成完整绝对路径
    goods_front_image = serializers.ImageField()
