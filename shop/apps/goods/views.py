from django.shortcuts import render
from .serializers import GoodsSerializer

from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics

from .models import Goods


# GenericAPIView 继承自views.APIView，并进行了一层封装
class GoodsListView(generics.ListAPIView):
    """
    商品列表页
    """
    queryset = Goods.objects.all()[:10]
    serializer_class = GoodsSerializer
