# -*- coding:utf-8 -*-
from datetime import datetime


from django.db import models


# 课程学院信息
class CourseCollege(models.Model):
    campus = models.CharField(max_length=20, verbose_name='校区', choices=(('dxq', '东校区'), ('xxq', '西校区'), ('ytxq', '烟台校区')), default='dxq')
    name = models.CharField(max_length=50, verbose_name='学院名称')
    desc = models.TextField(verbose_name='学院描述')
    tag = models.CharField(max_length=10, verbose_name='学院标签', default='世界闻名')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='media/college/%Y/%m', verbose_name='logo', max_length=100)
    address = models.CharField(max_length=150, verbose_name='学院地址')    
    student_nums = models.IntegerField(default=0, verbose_name='学习人数')
    courses_nums = models.IntegerField(default=0, verbose_name='课程数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '学院'
        verbose_name_plural = verbose_name

    # 获取学院下属的教师数量
    def get_teacher_nums(self):
        return self.teacher_set.all().count()
    get_teacher_nums.short_description = '教师数'

    # 获取学院开设的课程数量
    def get_course_nums(self):
        return self.course_set.all().count()
    get_course_nums.short_description = '课程数'

    def __str__(self):
        return self.name


# 学院教师信息
class Teacher(models.Model):
    college = models.ForeignKey(CourseCollege, verbose_name='所属学院')
    name = models.CharField(max_length=50, verbose_name='教师名称')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_position = models.CharField(max_length=50, verbose_name='教师职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    age = models.IntegerField(default=18, verbose_name='教师年龄')
    image = models.ImageField(default='', upload_to='media/teacher/%Y/%m', verbose_name='头像', max_length=100)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    # 获取教师教授的课程数量
    def get_course_nums(self):
        return self.course_set.all().count()

    def __str__(self):
        return self.name

# # 校区信息
# class Campus(models.Model):
#     name = models.CharField(max_length=20, verbose_name='校区', choices=(('dxq', '东校区'), ('xxq', '西校区'), ('ytxq', '烟台校区')), default='dxq')
#     desc = models.CharField(max_length=200, verbose_name='描述')
#     add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
#
#     class Meta:
#         verbose_name = '校区'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name





