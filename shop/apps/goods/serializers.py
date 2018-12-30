# _*_ coding: utf-8 _*_
__author__ = 'ife'
__date__ = '2018-12-30 18:33'

from rest_framework import serializers
from goods.models import Goods, GoodsCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    # 自己定义字段覆盖原有字段
    category = CategorySerializer()

    class Meta:
        model = Goods
        fields = "__all__"  # 将所有字段全部取出来
