from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from areas import serializers
from areas.models import Area
from areas.serializers import AreasSerializer, SubAreaSerializer


class AreasViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    行政区划信息
    """
    # 区划信息不分页
    pagination_class = None

    def get_queryset(self):
        """
        提供数据集
        """
        if self.action == 'list':
            return Area.objects.filter(parent=None)
        else:
            return Area.objects.all()

    def get_serializer_class(self):
        """
        提供序列化器
        """
        if self.action == 'list':
            return AreasSerializer
        else:
            return SubAreaSerializer

#
# class AreasView(ListAPIView):
#     """
#
#     """
#     serializer_class = serializers.AreasSerializer
#
#     queryset = Area.objects.filter(parent=None)
#
#
# class AreaView(GenericAPIView):
#     """
#
#     """
#     serializer_class = serializers.SubAreaSerializer
#
#     queryset = Area.objects.all()


