from django.shortcuts import render
from .serializers import GoodsSerializer
# from rest_framework.views import APIView

from rest_framework.response import Response
# from rest_framework import status
from rest_framework import mixins
from rest_framework import generics

from .models import Goods


# GenericAPIView 继承自views.APIView，并进行了一层封装
class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):
    """
    商品列表页
    """
    queryset = Goods.objects.all()[:10]
    serializer_class = GoodsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # def post(selfs, request, farmat=None):
    #     serializer = GoodsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

