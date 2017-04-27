# -*- coding:utf-8 -*-
from random import Random
from django.core.mail import send_mail

from user_member.models import EmailVerifyRecord
from CAU_Mooc.settings import EMAIL_FROM


# 生成随机的 指定 长度的字符串(由数字和大小写字母组成)，默认为 16位
def random_str(randomlength=16):
    code = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        code += chars[random.randint(0, length)]
    return code


# 发生邮件，默认发送类型为 【注册激活】
def send_register_email(email, send_type="register"):
    # 实例化一个 EmailVerifyRecord 邮箱验证码对象 email_record，用于将数据 insert 到数据库中
    email_record = EmailVerifyRecord()
    # 如果发送类型为 【更新邮箱】，则生成 4位 长度的随机字符串
    if send_type == "update_email":
        code = random_str(4)
    # 否则，生成 16位 长度的字符串
    else:
        code = random_str(16)
    # 使用 email_record 实例储存数据并插入数据库
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    # 如果发送类型为 【注册激活】
    if send_type == "register":
        # 邮件主题
        email_title = "caux-online注册激活链接"
        # 邮件内容
        email_body = "请点击下边的链接，激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)
        # send_mail() 的四个参数分别是 邮件主题，邮件内容，邮件发件人，邮件收件人 list
        # 该方法的返回值为邮件发生成功的数量(0 或者 1)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    # 如果发送类型为 【忘记密码】
    elif send_type == "forget":
        email_title = "caux-online密码重置链接"
        email_body = "请点击下边的链接重置密码：http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    # 如果发送类型为 【更新邮箱】
    elif send_type == "update_email":
        email_title = "caux-online邮箱修改验证码"
        email_body = "你的邮箱验证码为: {0}".format(code[:4])
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        if send_status:
            pass


