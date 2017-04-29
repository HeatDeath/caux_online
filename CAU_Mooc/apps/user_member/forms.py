# -*- coding:utf-8 -*-
from django import forms
from captcha.fields import CaptchaField

from .models import PersonalInformation


# 预处理 【登录】 表单验证
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


# 预处理 【注册】 表单验证
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    # 【验证码】验证
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


# 预处理 【忘记密码】 表单验证
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


# 预处理 【修改密码】 表单验证
class ResetPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


# 预处理 【用户个人主页】 表单验证
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInformation
        fields = ['nick_name', 'birthday', 'mobile', 'gender', 'address']


# 预处理 【上传头像】 表单验证
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = PersonalInformation
        fields = ['image', ]


