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


# 学院列表显示 View
# ## ---- 本 view 功能已通过测试 ---- ## 取出 hot_colleges并显示，使用 sort 排序，分页功能 正常
class CollegeListView(View):
    def get(self, request):
        # 获取数据库中全部的 学院 对象
        all_college = CourseCollege.objects.all()
        # 将全部学院对象按照 点击数 倒叙排列，取出前 3 位作为热点学院
        hot_colleges = all_college.order_by('-click_nums')[:3]
        # 取出 GET 请求中的 search_keywords
        search_keywords = request.GET.get('keywords', '')
        # 如果存在 search_keywords 检索关键词
        if search_keywords:
            # 使用检索关键词对全部 学院 对象进行过滤
            all_college = all_college.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))
        # 取出 GET 请求中的 sort
        sort = request.GET.get('sort', '')
        # 如果存在 sort 指定排序
        if sort:
            # 如果指定以 student_nums 学生数量进行排序
            if sort == 'student_nums':
                # 将学院按照 student_nums 学生数量进行到序排列
                all_college = all_college.order_by('-student_nums')
            # 如果指定以 course_nums 学生数量进行排序
            elif sort == 'course_nums':
                # 将学院按照 course_nums 学生数量进行到序排列
                all_college = all_college.order_by('course_nums')
        # 统计学院的数量
        college_nums = all_college.count()
        # 当前导航设置为 college 学院
        current_nav = 'college'

        # 分页器
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 数字 2 为当前每页显示的 college 的数量
        p = Paginator(all_college, 2, request=request)
        colleges = p.page(page)

        return render(request, 'college/college-list.html', {
            'all_college': colleges,
            'college_nums': college_nums,
            'hot_colleges': hot_colleges,
            'sort': sort,
            'current_nav': current_nav,
        })


# 学院主页显示 View
# ## ---- 本 view 功能已通过测试 ---- ## 解析学院 id，设置当前页，增加学院点击数，验证用户信息,用户收藏学院功能 正常
class CollegeHomeView(View):
    def get(self, request, college_id):
        # 通过当前 GET 请求中的 college_id 获取对应的 学院 对象
        course_college = CourseCollege.objects.get(id=int(college_id))
        # 设置 current_page 为 home 学院主页
        current_page = 'home'
        # 每当有对该学院主页的 GET 请求的时候， 该学院的 点击数 +1
        course_college.click_nums += 1
        # 修改后的该学院数据
        course_college.save()
        # has_fav 是否收藏置为 False
        has_fav = False
        # 如果当前发送 request 请求的 user 用户已经 is_authenticated() 经过身份验证
        if request.user.is_authenticated():
            # 如果可以在 UserFavorite 表中找到该 request.user 收藏 course_college.id 该学院的收藏信息
            if UserFavorite.objects.filter(user=request.user, fav_id=course_college.id, fav_type=2):
                # 则 hav_fav 已收藏置为 True
                has_fav = True
        # 因为 Course 表的 course_college 字段为外键，指向 CourseCollege 表
        # 所以可以通过此外键取出 一个 college 所对应的全部的 course 对象
        all_course = course_college.course_set.all()[:3]
        # 同理可以取出 一个 college 所对应的全部的 teacher 对象
        all_teacher = course_college.teacher_set.all()[:1]
        return render(request, 'college/college-detail-homepage.html', {
            'all_course': all_course,
            'all_teacher': all_teacher,
            'course_college': course_college,
            'current_page': current_page,
            'has_fav': has_fav,
        })


# 学院介绍页 View
# ## ---- 本 view 功能已通过测试 ---- ## 解析学院 id，设置当前页，验证用户信息,用户收藏学院功能 正常
class CollegeDescView(View):
    def get(self, request, college_id):
        course_college = CourseCollege.objects.get(id=int(college_id))
        current_page = 'desc'
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_college.id, fav_type=2):
                has_fav = True
        return render(request, 'college/college-detail-desc.html', {
            'course_college': course_college,
            'current_page': current_page,
            'has_fav': has_fav,
        })


# 学院课程页 View
# ## ---- 本 view 功能已通过测试 ---- ## 解析学院 id，设置当前页，验证用户信息,用户收藏学院功能 正常
class CollegeCourseView(View):
    def get(self, request, college_id):
        course_college = CourseCollege.objects.get(id=int(college_id))
        current_page = 'course'
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_college.id, fav_type=2):
                has_fav = True
        all_course = course_college.course_set.all()
        return render(request, 'college/college-detail-course.html', {
            'all_course': all_course,
            'course_college': course_college,
            'current_page': current_page,
            'has_fav': has_fav,
        })


# 学院教师页 View
# ## ---- 本 view 功能已通过测试 ---- ## 解析学院 id，设置当前页，验证用户信息,用户收藏学院功能 正常
class CollegeTeacherView(View):
    def get(self, request, college_id):
        course_college = CourseCollege.objects.get(id=int(college_id))
        current_page = 'teacher'
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_college.id, fav_type=2):
                has_fav = True
        all_teacher = course_college.teacher_set.all()
        return render(request, 'college/college-detail-teacher.html', {
            'all_teacher': all_teacher,
            'course_college': course_college,
            'current_page': current_page,
            'has_fav': has_fav,
        })


# 用户咨询 View
# ## ---- 本 view 功能已通过测试 ---- ## 验证 POST 数据有效性，并保存 POST 数据，提示添加失败功能 正常
class UserAskView(View):
    def post(self, request):
        # 实例化一个 UserAskForm 对象 user_ask_form 存放用户 POST 的数据
        user_ask_form = UserAskForm(request.POST)
        res = dict()
        # 验证用户 POST 数据的有效性
        if user_ask_form.is_valid():
            # 如果通过验证 提交 并 保存 数据
            user_ask_form.save(commit=True)
            res['status'] = 'success'
        else:
            res['status'] = 'fail'
            res['msg'] = '添加失败'
        return HttpResponse(json.dumps(res), content_type='application/json')


# 用户收藏 View
# ## ---- 本 view 功能已通过测试 ---- ## 判定用户登录，收藏和取消收藏，加减收藏数量功能 正常
class UserFavView(View):
    def post(self, request):
        # 获取用户 POST 数据中的 fav_id ， 默认为 0
        fav_id = int(request.POST.get('fav_id', 0))
        # 获取用户 POST 数据中的 fav_type ， 默认为 0
        fav_type = int(request.POST.get('fav_type', 0))
        res = dict()
        # 判定用户是否已经登录
        if not request.user.is_authenticated():
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            # res['msg'] = '请登陆后再使用收藏功能！'
            return HttpResponse(json.dumps(res), content_type='application/json')
        # 通过 user，fav_id，fav_type 在 UserFavorite 表中查询，是否已经存在该条 收藏记录
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
        # 若该 收藏记录 已经存在
        if exist_records:
            # 删除该条 收藏记录
            exist_records.delete()
            # 当 fav_type 为 1 ，即 收藏类型 为 课程 时
            if int(fav_type) == 1:
                # 通过 fav_id 找到这门 课程
                course = Course.objects.get(id=int(fav_id))
                # 该课程的收藏数量 -1
                course.fav_nums -= 1
                # 当课程的收藏数量 < 0 时，将其置为 0
                if course.fav_nums < 0:
                    course.fav_nums = 0
                # 保存该门课程的数据
                course.save()

            # 当 fav_type 为 2 ，即 收藏类型 为 学院 时
            elif int(fav_type) == 2:
                # 通过 fav_id 找到这个 学院
                course_college = CourseCollege.objects.get(id=int(fav_id))
                course_college.fav_nums -= 1
                if course_college.fav_nums < 0:
                    course_college.fav_nums = 0
                course_college.save()

            # 当 fav_type 为 3 ，即 收藏类型 为 教师 时
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            # self.set_fav_nums(fav_type, fav_id, -1)
            res['status'] = 'success'
            res['msg'] = '收藏'
        # 若该 收藏记录 不存在
        else:
            # 实例化一个 UserFavorite 对象 user_fav
            user_fav = UserFavorite()
            # 当 fav_id 和 fav_type 存在（即不为 0）的时候
            if fav_id and fav_type:
                # 设置该实例的 user 为 request.user
                user_fav.user = request.user
                # 设置该实例的 fav_id 为用户 POST 的 fav_id
                user_fav.fav_id = fav_id
                # 设置该实例的 fav_type 为用户 POST 的 fav_type
                user_fav.fav_type = fav_type
                # 保存修改的数据
                user_fav.save()
                # 当 fav_type 收藏类型为 1 的时候
                if int(fav_type) == 1:
                    # 获取对应的课程
                    course = Course.objects.get(id=int(fav_id))
                    # 收藏数 +1
                    course.fav_nums += 1
                    # 保存数据
                    course.save()
                elif int(fav_type) == 2:
                    course_college = CourseCollege.objects.get(id=int(fav_id))
                    course_college.fav_nums += 1
                    course_college.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                # self.set_fav_nums(fav_type, fav_id, 1)
                res['status'] = 'success'
                res['msg'] = '已收藏'
            else:
                res['status'] = 'fail'
                res['msg'] = '收藏出错'
        return HttpResponse(json.dumps(res), content_type='application/json')


# 教师列表页 View
# ## ---- 本 view 功能已通过测试 ---- ## 检索，排序，排名，分页功能 正常
class TeacherListView(View):
    def get(self, request):
        # 获取全部 教师 对象
        all_teacher = Teacher.objects.all()
        # 从 GET 请求中获取 keywords 检索关键词
        search_keywords = request.GET.get('keywords', '')
        # 如果存在 search_keywords 检索关键词
        if search_keywords:
            # 通过过滤得到 名字 中 包含 search_keywords 的 教师 对象
            all_teacher = all_teacher.filter(name__icontains=search_keywords)
        # 从 GET 请求中获取 sort 排序要求
        sort = request.GET.get('sort', '')
        # 如果存在 sort
        if sort:
            # 当 sort 为 hot ，即按照 教师 的 click_nums 点击数 排序
            if sort == 'hot':
                # 将 全部 教师 对象按照 点击数 倒叙 排列
                all_teacher = all_teacher.order_by('-click_nums')
        # 获取 点击数 排名 前三 的 教师 对象
        sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:3]

        # 分页器
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teacher, 5, request=request)
        teachers = p.page(page)

        return render(request, 'college/teacher-list.html', {
            'all_teacher': teachers,
            'sorted_teachers': sorted_teachers,
            'sort': sort,
        })


# 教师个人详情页 View
# ## ---- 本 view 功能已通过测试 ---- ## 教师收藏数统计，登录验证，收藏状态判断功能 正常
class TeacherDetailView(View):
    def get(self, request, teacher_id):
        # 每当 GET 请求到此 teacher_id 时， 该教师的 点击数 +1
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.click_nums += 1
        # 保存修改的数据
        teacher.save()
        # 取出全部该 teacher_id 对应的教师的全部 课程 对象
        all_course = Course.objects.filter(teacher=teacher)
        # 收藏教师 与 收藏学院 的默认状态为 False
        has_fav_teacher = False
        has_fav_college = False
        # 如果本次 请求 来自于已登录的用户
        if request.user.is_authenticated():
            # 检查该用户是否收藏了该名 教师 及 与该教师 对应的学院
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.college.id):
                has_fav_college = True
        # 获取 点击数 排名前三 的 教师 对象
        sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:3]
        return render(request, 'college/teacher-detail.html', {
            'teacher': teacher,
            'all_course': all_course,
            'sorted_teachers': sorted_teachers,
            'has_fav_teacher': has_fav_teacher,
            'has_fav_college': has_fav_college,
        })






