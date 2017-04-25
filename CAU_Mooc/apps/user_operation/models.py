# -*- coding:utf-8 -*-
from datetime import datetime


from django.db import models


from user_member.models import PersonalInformation
from mooc_course.models import Course


# 用户咨询表
class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    course_name = models.CharField(max_length=50, verbose_name='课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name


# 用户课程评论表
class UserCourseComment(models.Model):
    user = models.ForeignKey(PersonalInformation, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')
    comment = models.CharField(max_length=200, verbose_name='评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name


# 用户的收藏表
class UserFavorite(models.Model):
    user = models.ForeignKey(PersonalInformation, verbose_name='用户')
    # ID 是课程的 ID 或者是 讲师、课程机构的 ID
    fav_id = models.IntegerField(default=0, verbose_name='收藏数据 Id')
    fav_type = models.IntegerField(choices=((1, '课程'), (2, '学院'), (3, '讲师')), default=1, verbose_name='收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


# 用户接收消息表
class UserMessage(models.Model):
    # 如果为 0 代表全局消息，否则就是用户的 ID
    user = models.IntegerField(default=0, verbose_name='接受用户')
    message = models.CharField(max_length=500, verbose_name='消息内容')
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message


# 用户学习课程表
class UserCourse(models.Model):
    user = models.ForeignKey(PersonalInformation, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户学习的课程'
        verbose_name_plural = verbose_name

