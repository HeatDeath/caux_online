# -*- coding:utf-8 -*-
import xadmin


from .models import CourseCollege, Teacher


# # 后台 【校区】 管理
# class CampusAdmin(object):
#     # 后台自定义显示列
#     list_display = ['name', 'desc', 'add_time']
#     # 定义后台搜索
#     search_fields = ['name', 'desc']
#     # 通过时间搜索
#     list_filter = ['name', 'desc', 'add_time']
#     relfield_style = 'fk-ajax'


# 后台 【学院】 管理
class CourseCollegeAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'get_course_nums', 'get_teacher_nums']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums']

    # 只有在搜索的时候，才会加载出来， 在数据量过大的时候，不会一次性加载出来
    # relfield_style = 'fk-ajax'


# 后台 【教师】 管理
class TeacherAdmin(object):
    list_display = ['college', 'name', 'work_years', 'work_position']
    search_fields = ['college', 'name', 'work_years', 'work_position']
    list_filter = ['college', 'name', 'work_years', 'work_position']


# xadmin.site.register(Campus, CampusAdmin)
xadmin.site.register(CourseCollege, CourseCollegeAdmin)
xadmin.site.register(Teacher, TeacherAdmin)

