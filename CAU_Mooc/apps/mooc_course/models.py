# -*- coding:utf-8 -*-
from datetime import datetime


from django.db import models


from cau_college.models import CourseCollege, Teacher


# 课程信息
class Course(models.Model):
    course_college = models.ForeignKey(CourseCollege, verbose_name='课程学院', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='课程名称')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    degree = models.CharField(verbose_name='课程难度', choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    student_nums = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name='封面图片', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    tag = models.CharField(default='', verbose_name='课程标签', max_length=10)
    category = models.CharField(max_length=20, verbose_name='课程类别', default='')
    advance_course = models.CharField(max_length=50, verbose_name='先修课程', default='')
    harvest = models.CharField(max_length=300, verbose_name='课程收获', default='')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    # 获取课程章节数量
    def get_zj_nums(self):
        return self.lesson_set.all().count()
    # 修改后台列名的显示，否则该列显示为 get_zj_nums
    get_zj_nums.short_description = '章节数'

    # 获取正在学习当前课程用户数量
    def get_user_nums(self):
        return self.usercourse_set.all().count()
    get_user_nums.short_description = '学生数'

    # 获取前五名正在学习本课程的用户
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    # 获取课程所包含的章节
    def get_course_lesson(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name


# 课程章节
class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    # 获取章节视频
    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


# 章节视频
class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名')
    url = models.CharField(max_length=200, verbose_name='访问地址', default='')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 课程资源
class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

