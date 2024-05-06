
from django.contrib import admin
from django.urls import path
from wechatapp.views import handle as wechat_route

urlpatterns = [
    path('getwechatinfo/', wechat_route),
]
