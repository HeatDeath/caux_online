# -*- coding:utf-8 -*-
from django.conf.urls import url, include


from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, \
                   MyCourseView, MyFavCollegeView, MyFavTeacherView, MyFavCourseView, MyMessageView

urlpatterns = [
    # 配置 user/info/ 用户个人主页的 url
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),

    # 配置 user/image/upload/ 用户个人头像上传的 url
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),

    # 配置 user/update/pwd/ 用户修改个人密码的 url
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),

    # 配置 user/sendemail_code/ 用户修改邮箱时验证码的 url
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),

    # 配置 user/update_email/ 用户修改个人邮箱的 url
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    # 配置 user/mycourse/ 用户正在学习课程的 url
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),

    # 配置 user/myfav/college/ 用户收藏学院的 url
    url(r'^myfav/college/$', MyFavCollegeView.as_view(), name='myfav_college'),

    # 配置 user/myfav/teacher/ 用户收藏教师的 url
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),

    # 配置 user/myfav/course/ 用户收藏课程的 url
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),

    # 配置 user/mymessage/ 用户个人消息的 url
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),

]