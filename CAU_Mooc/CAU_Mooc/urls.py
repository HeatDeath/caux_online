import xadmin
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve #处理静态文件


from CAU_Mooc.settings import MEDIA_ROOT
from user_member.views import LoginView, IndexView, RegisterView, ActiveUserView, ForgetView, \
                              ResetPwdView, LogoutView



urlpatterns = [
    # 配置 xadmin 后台管理页面的 url
    url(r'^admin/', xadmin.site.urls),
    # 配置 index 首页的 url
    url(r'^$', IndexView.as_view(), name='index'),
    # 配置 login 登录页面的 url
    url(r'^login/$', LoginView.as_view(), name='login'),
    # 配置 login 登录页面的 url
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    # 配置 register 用户注册页面的 url
    url(r'^register/$', RegisterView.as_view(), name='register'),
    # 配置 active 用户注册激活页面的 url，使用正则表达式中的捕获组来获取 url 中的变量(active_code)
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    # 配置 forget 用户忘记密码页面的 url
    url(r'^forget/$', ForgetView.as_view(), name='forget_pwd'),
    # 用户在邮件里点击重置密码链接
    url(r'^reset/(?P<active_code>.*)/$', ResetPwdView.as_view(), name='reset_url'),
    # 重置密码表单 POST 请求
    url(r'^modify_pwd/$', ResetPwdView.as_view(), name='modify_pwd'),
    # 配置 captcha 验证码生成工具的 url
    url(r'^captcha/', include('captcha.urls')),
    # 配置 college 学院 App 的 url
    url(r'^college/', include('cau_college.urls', namespace='college')),
    # 配置 course 课程 App 的 url
    url(r'^course/', include('mooc_course.urls', namespace='course')),
    # 配置 user 用户 App的 url
    url(r'^users/', include('user_member.urls', namespace='users')),
    # 配置 media 上传文件访问处理 url
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

]


# 全局 404,500 页面配置
handler404 = 'site_manage.views.page_not_found'
handler500 = 'site_manage.views.page_error'
