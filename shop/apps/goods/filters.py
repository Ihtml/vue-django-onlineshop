# _*_ coding: utf-8 _*_
__author__ = 'ife'
__date__ = '2019-01-02 22:40'

import django_filters
from django.db.models import Q

from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    pricemin = django_filters.NumberFilter(field_name='shop_price', help_text="最低价格",lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name='shop_price', help_text="最高价格", lookup_expr='lte')
    # 模糊查询
    # name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    # 自定义filter,查找第一类别下面所有商品
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot', 'is_new']
