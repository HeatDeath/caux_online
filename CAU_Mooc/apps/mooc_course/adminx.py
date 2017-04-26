# -*- coding:utf-8 -*-
import xadmin


from .models import Course, Lesson, Video, CourseResource


# 后台 【课程】 管理
class CourseAdmin(object):
    # 后台展示字段
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student_nums', 'fav_nums', 'image',
                    'click_nums', 'add_time', 'get_zj_nums']
    # 后台搜索字段
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student_nums', 'fav_nums', 'image', 'click_nums']
    # 后来字段过滤器
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student_nums', 'fav_nums', 'image', 'click_nums',
                   'add_time']
    # 后台显示顺序
    ordering = ['-click_nums']


# 后台 【章节】 管理
class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    # course 是一个对象，xadmin 不能搜索，需要指定搜索 course 对象里哪一个属性
    list_filter = ['course__name', 'name', 'add_time']


# 后台 【视频】 管理
class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


# 后台 【课程资源】 管理
class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)