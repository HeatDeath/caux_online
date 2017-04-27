import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.backends import ModelBackend
from django.core.urlresolvers import reverse


from .models import PersonalInformation, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ResetPwdForm
from site_manage.models import Banner
from utils.email_send import send_register_email


# 继承 django.contrib.auth.backends 的 ModelBackend，并重写，实现使用可以同时使用 用户名 或者 邮箱 登录的功能
# ## ---- 本 class 功能已通过测试 ---- ## 使用用户名和邮箱皆可登录
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 用 Q 实现并集查询
            user = PersonalInformation.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 用户登录 View
# ## ---- 本 view 功能已通过测试 ---- ## form 验证， authenticate 验证，错误提示功能 正常
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        # 实例化一个 LoginForm 对象
        login_form = LoginForm(request.POST)
        # 验证 POST 提交的每个参数是否有效
        if login_form.is_valid():
            # 通过 html 页面的 input 标签的 name 属性的值 username 来获取用户提交的 username
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            # 使用 authenticate() 验证用户名和密码是否与数据库中的数据匹配
            # 如果匹配成功， 返回一个 user 对象。否则，返回 None
            user = authenticate(username=username, password=password)
            if user is not None:
                # 判断该用户是否已经激活
                if user.is_active:
                    # 使用 login() 登录该用户
                    login(request, user)
                    # 返回 Http 响应重定向到，反转名为 index 所指向的 url
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户尚未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或者密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


# 用户注销 View
# ## ---- 本 view 功能已通过测试 ---- ## 注销功能 正常
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


# 用户注册 View
# ## ---- 本 view 功能已通过测试 ---- ## form 验证，保存数据到数据库，向用户发送激活邮件，错误提示功能 正常
# 向新注册的用户发送欢迎消息功能尚未实现
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', '')
            # 如果该邮箱已经存在于数据库中
            if PersonalInformation.objects.filter(email=username):
                return render(request, 'register.html', {
                    'register_form': register_form,
                    'msg': '该邮箱已被注册',
                })
            password = request.POST.get('password', '')
            # 实例化一个 PersonalInformation 对象，用于将用户的注册信息 insert 到数据库中
            user_information = PersonalInformation()
            user_information.username = username
            user_information.email = username
            user_information.is_active = False
            user_information.password = make_password(password)
            user_information.save()

            # 向新注册的用户发送欢迎消息
            # ----------------------

            # 向新注册的用户发送激活邮件
            send_register_email(username, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {
                'register_form': register_form,
                'msg': '请输入正确的字段',
            })


# 新用户激活 View
# ## ---- 本 view 功能已通过测试 ---- ## 检查激活码对应的用户，并激活功能，新注册用户激活后登录功能 正常
class ActiveUserView(View):
    def get(self, request, active_code):
        # 通过 active_code 在 EmailVerifyRecord 表中过滤记录
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        # 如果该 active_code 存在于数据库中
        if all_record:
            # 遍历从数据库中，过滤得到的记录
            for record in all_record:
                # 找到该 active_code 对应的 email
                email = record.email
                # 找对该 email 对应的用户
                user = PersonalInformation.objects.get(email=email)
                # 将该用户的 【激活状态】 改为 【已激活】
                user.is_active = True
                # 保存
                user.save()
        # 如果该 active_code 不存在
        else:
            # 返回链接失效页面
            return render(request, 'active_file.html')
        # 用户成功激活，返回登录页面
        return render(request, 'login.html')


# 用户找回密码 View
# ## ---- 本 view 功能已通过测试 ---- ## form 验证，向用户发送重置密码邮件，错误提示功能 正常
class ForgetView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {
            'forget_form': forget_form,
        })

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        # 验证用户提交表单的数据有效性
        if forget_form.is_valid():
            # 获取用户提交的 email
            email = request.POST.get('email', '')
            # 向该 email 地址发送重置密码的邮件
            send_register_email(email, 'forget')
            # 返回发送成功的页面
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {
                'forget_form': forget_form,
                # 'msg': '请提交有效的数据',
            })


# 用户重置密码 View
# ## ---- 本 view 功能已通过测试 ---- ## form 验证，通过重置密码邮件重置密码，错误提示功能 正常
class ResetPwdView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})

    def post(self, request):
        resetpwd_form = ResetPwdForm(request.POST)
        email = request.POST.get('email', '')
        if resetpwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {
                    'email': email,
                    'msg': '两次输入的密码不一致！'
                })
            user = PersonalInformation.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html')
        return render(request, 'password_reset.html', {
            'email': email,
            'resetpwd_form': resetpwd_form,
        })


# 首页 View
class IndexView(View):
    def get(self, request):
        all_banner = Banner.objects.all().order_by('index')
        # courses = Course.objects.filter(is_banner=False)[:6]
        # banner_courses = Course.objects.filter(is_banner=True)[:3]
        # course_colleges = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banner': all_banner,
            'courses': '',
            'banner_courses': '',
            'course_colleges': '',
        })

