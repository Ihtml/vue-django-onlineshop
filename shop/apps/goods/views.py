from django.shortcuts import render
from .serializers import GoodsSerializer

from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from .models import Goods
from .filters import GoodsFilter


# 定制化分页
class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'p' # 默认为 "next": "http://localhost:8000/goods/?page=2",
    max_page_size = 100


# GenericAPIView 继承自views.APIView，并进行了一层封装
class GoodsListViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    商品列表页
    """
    queryset = Goods.objects.all()
    pagination_class = GoodsPagination
    serializer_class = GoodsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')

    # def get_queryset(self):
    #     queryset = Goods.objects.all()
    #     # price_min为前端的请求参数，默认为0
    #     price_min = self.request.query_params.get('price_min', 0)
    #     if price_min:
    #         queryset = queryset.filter(shop_price__gt=int(price_min))
    #     return queryset
