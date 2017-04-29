from django.shortcuts import render_to_response


# 全局 404 处理函数
def page_not_found(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


# 全局 500 处理函数
def page_error(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
