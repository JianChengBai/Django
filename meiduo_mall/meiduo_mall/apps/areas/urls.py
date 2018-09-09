from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from areas import views

urlpatterns = [
    url(r'^areas/$', views.AreasView.as_view()),
    url(r'^areas/(?P<pk>\d+)/$', views.AreaView.as_view())

]
# # 给视图集生成路由
# router = DefaultRouter()
# # router.register("路由前缀"，"视图集类"，"别名前缀")
# router.register(r'areas', views.AreasViewSet, base_name='areas')
#
# urlpatterns = []
#
# urlpatterns += router.urls

