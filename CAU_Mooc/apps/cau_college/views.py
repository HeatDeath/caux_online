import json
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseCollege, Teacher
from .forms import UserAskForm
from mooc_course.models import Course
from user_operation.models import UserFavorite


class CollegeView(View):
    def get(self, request):
        all_college = CourseCollege.objects.all()
        hot_colleges = all_college.order_by('-click_nums')[:3]
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_college = all_college.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        sort = request.POST.get('sort', '')
        if sort:
            if sort == 'student_nums':
                all_college = all_college.order_by('-student_nums')
            elif sort == 'course_nums':
                all_college = all_college.order_by('course_nums')

        college_nums = all_college.count()
        current_nav = 'college'
        # 分页器
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_college, 5, request=request)
        colleges = p.page(page)

        return render(request, 'college-list.html', {
            'all_college': colleges,
            'college_nums': college_nums,
            'hot_colleges': hot_colleges,
            'sort': sort,
            'current_nav': current_nav,
        })


# 用户添加咨询课程表单提交
class AddUserAskView(View):
    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        res = dict()
        if user_ask_form.is_valid():
            user_ask_form.save(commit=True)
            res['status'] = 'success'
        else:
            res['status'] = 'fail'
            res['msg'] = '添加出错'
        return HttpResponse(json.dumps(res), content_type='application/json')





