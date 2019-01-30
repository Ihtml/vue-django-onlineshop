# _*_ coding: utf-8 _*_
__author__ = 'ife'
__date__ = '2019-01-30 22:48'

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # 如果是安全的方法就直接返回TRUE
        if request.method in permissions.SAFE_METHODS:
            return True

        # 否则就判断是不是user
        # Instance must have an attribute named `owner`.
        return obj.user == request.user
