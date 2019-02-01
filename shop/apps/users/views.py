from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from rest_framework import viewsets
from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from random import choice
from shop.settings import APIKEY
from utils.yunpian import YunPian
from .models import VerifyCode
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证,用户名和手机号
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    1,验证是不是合法的手机号
    2，手机号是否注册过
    3，短信验证码验证
    """

    # serializer_class - 用于验证和反序列化输入以及序列化输出的序列化类。
    # 通常必须设置此属性，或覆盖 get_serializer_class() 方法。
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = '0123456789'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        # 获取相关serializer
        serializer = self.get_serializer(data=request.data)
        # 如果验证失败，就会直接抛异常，而不会进入下面的代码
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(APIKEY)

        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        # 0代表成功
        if sms_status["code"] !=0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_recode = VerifyCode(code=code, mobile=mobile)
            code_recode.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """
    用户注册
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 重写get_object方法 可以返回当前用户
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()

