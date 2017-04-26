# -*- coding:utf-8 -*-
import xadmin


from .models import UserAsk, UserCourseComment, UserFavorite, UserMessage, UserCourse


# 后台 【用户咨询】 管理
class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']


# 后台 【课程评论】 管理
class CourseCommentAdmin(object):
    list_display = ['user', 'course', 'comment', 'add_time']
    search_fields = ['user', 'course', 'comment']
    list_filter = ['user__nick_name', 'course__name', 'comment', 'add_time']


# 后台 【用户收藏】 管理
class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user__nick_name', 'fav_id', 'fav_type', 'add_time']


# 后台 【用户消息】 管理
class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    # 这里的 user 不是 ForeignKey ，具体请看 models.py
    list_filter = ['user', 'message', 'has_read', 'add_time']


# 后台 【用户课程】 管理
class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user__nick_name', 'course__name', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourseComment, CourseCommentAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)

