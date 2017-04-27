# -*- coding:utf-8 -*-
from django.conf.urls import url

from .views import CollegeView, AddUserAskView

urlpatterns = [
    # 配置 /college/list/ 课程学院列表页 url
    url(r'^list/$', CollegeView.as_view(), name='college_list'),
    # 配置 /college/add_ask/ 用户咨询页 url
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
]