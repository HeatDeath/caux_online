# -*- coding:utf-8 -*-
import xadmin


from .models import PersonalInformation, EmailVerifyRecord


# 后台【邮箱验证码】管理
class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-rocket'


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)

