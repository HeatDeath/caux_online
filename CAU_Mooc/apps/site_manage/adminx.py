# -*- coding:utf-8 -*-
import xadmin
from xadmin import views


from .models import Banner


# 后台 【基础设置】
class BaseSetting(object):
    # 开启后台 【主题切换】 功能
    enable_themes = True
    use_bootswatch = True


# 后台 【全局设置】
class GlobalSettings(object):
    # 设置站点 title
    site_title = 'caux后台管理系统'
    # 设置站点 footer
    site_footer = 'cuax在线'
    # 设置 左侧菜单栏 为手风琴（折叠样式）
    menu_style = 'accordion'


# 后台 【首页轮播图】 管理
class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']
    # 设置后台左侧菜单的 【小图标】
    # model_icon = 'fa fa-rocket'


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Banner, BannerAdmin)

