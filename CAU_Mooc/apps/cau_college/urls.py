# -*- coding:utf-8 -*-
from django.conf.urls import url

from .views import CollegeListView, UserAskView, CollegeHomeView, CollegeCourseView, CollegeDescView, \
                   CollegeTeacherView, UserFavView, TeacherListView, TeacherDetailView

urlpatterns = [
    # 配置 /college/list/ 课程学院列表页 url
    url(r'^list/$', CollegeListView.as_view(), name='college_list'),
    # 配置 /college/add_ask/ 用户咨询页 url
    url(r'^add_ask/$', UserAskView.as_view(), name='add_ask'),
    url(r'^add_fav/$', UserFavView.as_view(), name='add_fav'),

    # 配置 /college/home/college_id/ 学院主页 url
    url(r'^home/(?P<college_id>\d+)/$',    CollegeHomeView.as_view(), name='college_home'),

    # 配置 /college/desc/college_id/ 学院介绍页 url
    url(r'^desc/(?P<college_id>\d+)/$',    CollegeDescView.as_view(), name='college_desc'),

    # 配置 /college/course/college_id/ 学院课程页 url
    url(r'^course/(?P<college_id>\d+)/$',  CollegeCourseView.as_view(), name='college_course'),

    # 配置 /college/teacher/college_id/ 学院教师页 url
    url(r'^teacher/(?P<college_id>\d+)/$', CollegeTeacherView.as_view(), name='college_teacher'),

    # 配置 /college/teacher/list/  教师列表页 url
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),

    # 配置 /college/teacher/detail/teacher_id/ 教师详情页 url
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),

]