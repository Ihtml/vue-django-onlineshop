# _*_ coding: utf-8 _*_
__author__ = 'ife'
__date__ = '2019-01-02 22:40'

import django_filters
from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    pricemin = django_filters.NumberFilter(field_name='shop_price', help_text="最低价格",lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name='shop_price', help_text="最高价格", lookup_expr='lte')
    # 模糊查询
    # name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot', 'is_new']
