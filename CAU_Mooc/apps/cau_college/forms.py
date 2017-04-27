# -*- coding:utf-8 -*-
import re
from django import forms


from user_operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    # 使用 re 检验 mobile 是否合法
    def clean_mobile(self):
        # 手机号验证
        mobile = self.cleaned_data['mobile']
        p = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        if p.match(mobile):
            # 这里还能返回外键
            return mobile
        raise forms.ValidationError('手机号码格式不对', code='mobile_inval')

