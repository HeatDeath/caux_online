import json
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import Course, CourseResource, Video
from utils.mixin_utils import LoginRequiredMixin
from user_operation.models import UserFavorite, UserCourseComment, UserCourse


# 课程列表页 View
# ## ---- 本 view 功能已通过测试 ---- ## 时间，热门，人数排序，热门课程推荐功能 正常
class CourseListView(View):
    def get(self, request):
        # 取出所有 课程 对象 按照 添加时间 倒序排列
        all_course = Course.objects.all().order_by('-add_time')
        # 按照 点击数 取出排名前三的课程对象
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        # 从 GET 请求中 获取 keywords 检索关键词
        serach_keywords = request.GET.get('keywords', '')
        if serach_keywords:
            all_course = all_course.filter(Q(name__icontains=serach_keywords) | Q(desc__icontains=serach_keywords) |
                                           Q(detail__icontains=serach_keywords))
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_course = all_course.order_by('-student_nums')
            elif sort == 'hot':
                all_course = all_course.order_by('-click_nums')

        # 对课程列表页进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, 3, request=request)
        courses = p.page(page)

        return render(request, 'course/course-list.html', {
            'all_course': courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


# 课程详情页 View
# ## ---- 本 view 功能已通过测试 ---- ## 收藏状态，课程点击数，相关课程推荐，课程同学功能 正常
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_college = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_college.id, fav_type=2):
                has_fav_college = True
        # 通过后台的课程标签，向用户推荐相关课程
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request, 'course/course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_college': has_fav_college,
        })


# 课程的章节信息页 View
# ## ---- 本 view 功能已通过测试 ---- ## 收藏状态，课程点击数，相关课程推荐功能 正常
class LessonInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        # 通过 course_id 获取本次 request 的课程
        course = Course.objects.get(id=int(course_id))
        # 取出当前课程的 all_resource 所有资源
        all_resource = CourseResource.objects.filter(course=course)
        # 将当前登录用户 request.user 实例化为一个 UserCourse 对象 user_course
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        # 如果当前登录用户为 关联 该课程
        if not user_course:
            # 将当前登录用户 关联 到该课程
            user_course = UserCourse(user=request.user, course=course)
            # 保存数据
            user_course.save()
            # 课程的学生总数 +1
            course.student_nums += 1
            # 保存数据
            course.save()

        # 取出 学习 这门课程 的 所有 UserCourse 对象
        all_study_this_course = UserCourse.objects.filter(course=course)
        # 取出 所有 学习 这门课程 的 用户 id
        study_this_course_user_ids = [study_this_course.user.id for study_this_course in all_study_this_course]
        # 通过用户 id，取出所有学习这门课程的 学生 所学的 所有 课程 对象
        all_user_course = UserCourse.objects.filter(user_id__in=study_this_course_user_ids)
        # 取出这些 课程 对应的 id
        course_ids = [one_user_course.course.id for one_user_course in all_user_course]
        # 取出这些课程中 点击数 排名 前五 的 Course 对象
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        return render(request, 'course/course-lesson-info.html', {
            'course': course,
            'course_resources': all_resource,
            'relate_courses': relate_courses,
        })


# 课程评论页 View
# ## ---- 本 view 功能已通过测试 ---- ## 课程评论，课程资源显示功能 正常
class CommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resource = CourseResource.objects.filter(course=course)
        all_comment = UserCourseComment.objects.filter(course=course)
        # -----------------------------------------------------------
        user_course = UserCourse(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.student_nums += 1
            course.save()

        all_study_this_course = UserCourse.objects.filter(course=course)
        study_this_course_user_ids = [study_this_course.user.id for study_this_course in all_study_this_course]
        all_user_course = UserCourse.objects.filter(user_id__in=study_this_course_user_ids)
        course_ids = [one_user_course.course.id for one_user_course in all_user_course]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        # -----------------------------------------------------------
        return render(request, 'course/course-comment.html', {
            'course': course,
            'all_comment': all_comment,
            'all_resource': all_resource,
            'relate_courses': relate_courses,
        })


# 用户添加课程评论 View
# ## ---- 本 view 功能已通过测试 ---- ## 添加课程评论功能 正常
class AddCommentView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict()
        # if not request.user.is_authenticated():
        #     res['status'] = 'fail'
        #     res['msg'] = '用户未登陆'
        #     return HttpResponse(json.dumps(res), content_type='application/json')
        course_id = int(request.POST.get('course_id', 0))
        comment = request.POST.get('comment', '')
        if course_id and comment:
            course_comment = UserCourseComment()
            course_comment.course = Course.objects.get(id=course_id)
            course_comment.comment = comment
            course_comment.user = request.user
            course_comment.save()
            res['status'] = 'success'
            res['msg'] = u'添加成功'
        else:
            res['status'] = 'fail'
            res['msg'] = u'添加失败'
        return HttpResponse(json.dumps(res), content_type='application/json')


# 章节视频播放页面 View
class VideoPlayView(LoginRequiredMixin, View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        all_resource = CourseResource.objects.filter(course=course)
        # -----------------------------------------------------------
        user_course = UserCourse(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.student_nums += 1
            course.save()

        all_study_this_course = UserCourse.objects.filter(course=course)
        study_this_course_user_ids = [study_this_course.user.id for study_this_course in all_study_this_course]
        all_user_course = UserCourse.objects.filter(user_id__in=study_this_course_user_ids)
        course_ids = [one_user_course.course.id for one_user_course in all_user_course]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        # -----------------------------------------------------------
        return render(request, 'course/course-video-play.html', {
            'course': course,
            'all_resource': all_resource,
            'relate_courses': relate_courses,
            'video': video,
        })

