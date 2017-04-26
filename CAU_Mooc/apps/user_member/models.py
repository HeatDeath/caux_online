from datetime import datetime


from django.db import models
from django.contrib.auth.models import AbstractUser


# 用户个人信息表，继承自 auth App 的 AbstractUser 表
class PersonalInformation(AbstractUser):
    nick_name = models.CharField(verbose_name="昵称", max_length=50, default="")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(verbose_name="性别", max_length=10, choices=(("male", "男"), ("female", "女")), default="female")
    address = models.CharField(verbose_name="地址", max_length=100, default="")
    mobile = models.CharField(verbose_name="手机号", max_length=11, null=True, blank=True)
    image = models.ImageField(verbose_name="头像", upload_to="media/image/%Y/%m", default="media/image/default.png", max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


# 邮箱验证信息表
class EmailVerifyRecord(models.Model):
    code = models.CharField(verbose_name="邮箱验证码", max_length=20)
    email = models.EmailField(verbose_name="邮箱", max_length=50)
    send_type = models.CharField(verbose_name="验证码类型", choices=(("register", "注册"), ("forget", "找回密码"),
                                                                ("update_email", "修改邮箱")), max_length=15)
    send_time = models.DateTimeField(verbose_name="发送时间", default=datetime.now)

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name


