from django.shortcuts import render
from .serializers import GoodsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Goods


class GoodsListView(APIView):
    """
    List all goods
    """
    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        # many=True表示是个queryset对象,序列化为数组
        goods_serializer = GoodsSerializer(goods, many=True)
        return Response(goods_serializer.data)
