from django.http import HttpResponse


def index(request):
    return HttpResponse("欢迎访问我的博客首页！")