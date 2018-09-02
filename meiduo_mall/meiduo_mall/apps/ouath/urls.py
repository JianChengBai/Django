from django.conf.urls import url

from ouath import views

urlpatterns = [
    url(r'^qq/authorization/$', views.QQAuthURLView.as_view())
]

