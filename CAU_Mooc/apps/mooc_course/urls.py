# -*- coding:utf-8 -*-
from django.conf.urls import url, include

from .views import CourseListView, CourseDetailView, LessonInfoView, CommentView, AddCommentView, VideoPlayView

urlpatterns = [
    # 配置 /course/list/ 课程列表页的 url
    url(r'^list/$', CourseListView.as_view(), name='course_list'),

    # 配置 /course/detail/course_id/ 课程列表页的 url
    url(r'^detail/(?P<course_id>\d+)/$',  CourseDetailView.as_view(), name='course_detail'),

    # 配置 /course/info/course_id/ 课程列表页的 url
    url(r'^info/(?P<course_id>\d+)/$',    LessonInfoView.as_view(), name='lesson_info'),

    # 配置 /course/comment/course_id/ 课程列表页的 url
    url(r'^comment/(?P<course_id>\d+)/$', CommentView.as_view(), name='course_comment'),

    # 配置 /course/video/course_id/ 课程列表页的 url
    url(r'^video/(?P<video_id>\d+)/$',   VideoPlayView.as_view(), name='video_play'),

    # 配置 /course/add_comment/ 课程列表页的 url
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
]