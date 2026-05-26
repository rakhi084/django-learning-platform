from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# HOME PAGE

def home(request):

    return render(request, 'home.html')


# REGISTER

def register_view(request):

    if request.method == "POST":

        username = request.POST['username']

        email = request.POST['email']

        password = request.POST['password']

        role = request.POST['role']
        profile_pic = request.FILES.get('profile_pic')

        User.objects.create_user(

            username=username,
            email=email,
            password=password,
            role=role,
            profile_pic=profile_pic
        )

        return redirect('login')

    return render(request, 'register.html')


# LOGIN
def login_view(request):

    if request.method == "POST":

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(

            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # INSTRUCTOR LOGIN

            if user.role == "instructor":

                return redirect(
                    'instructor_dashboard'
                )

            # STUDENT LOGIN

            elif user.role == "student":

                return redirect(
                    'student_dashboard'
                )

            # DEFAULT

            return redirect('home')

        else:

            context = {

                'error': 'Invalid Username or Password'

            }

            return render(

                request,
                'login.html',
                context
            )

    return render(

        request,
        'login.html'
    )
# LOGOUT

def logout_view(request):

    logout(request)

    return redirect('home')


# INSTRUCTOR DASHBOARD

def instructor_dashboard(request):

    if request.user.role != "instructor":

        return redirect('home')

    courses = Course.objects.filter(

        instructor=request.user
    )

    context = {

        'courses': courses

    }

    return render(

        request,
        'instructor_dashboard.html',
        context
    )


# CREATE COURSE

def create_course(request):

    if request.user.role != "instructor":

        return redirect('home')

    if request.method == "POST":

        title = request.POST['title']

        description = request.POST['description']

        course_type = request.POST['course_type']

        thumbnail = request.FILES['thumbnail']

        Course.objects.create(

            instructor=request.user,

            title=title,

            description=description,

            course_type=course_type,

            thumbnail=thumbnail
        )

        return redirect('instructor_dashboard')

    return render(
        request,
        'create_course.html'
    )



# ADD LESSON

# ADD LESSON

def add_lesson(request, course_id):

    if request.user.role != "instructor":

        return redirect('home')

    course = Course.objects.get(id=course_id)

    if request.method == "POST":

        title = request.POST['title']

        youtube_link = request.POST['youtube_link']

        Lesson.objects.create(

            course=course,

            title=title,

            youtube_link=youtube_link
        )

        return redirect('instructor_dashboard')

    context = {

        'course': course

    }

    return render(

        request,
        'add_lesson.html',
        context
    )


# COURSE DETAIL PAGE

def course_detail(request, course_id):

    course = Course.objects.get(id=course_id)

    lessons = course.lessons.all()

    enrolled = False

    if request.user.is_authenticated:

        enrolled = Enrollment.objects.filter(

            student=request.user,
            course=course

        ).exists()

    context = {

        'course': course,
        'lessons': lessons,
        'enrolled': enrolled

    }

    return render(

        request,
        'course_detail.html',
        context
    )


# ENROLL COURSE

def enroll_course(request, course_id):

    if not request.user.is_authenticated:

        return redirect('login')

    course = Course.objects.get(id=course_id)

    already_enrolled = Enrollment.objects.filter(

        student=request.user,
        course=course

    ).exists()

    if not already_enrolled:

        Enrollment.objects.create(

            student=request.user,
            course=course
        )
        Progress.objects.create(

        student=request.user,
        course=course
        )
    return redirect(

        'course_detail',
        course_id=course.id
    )


# LEARN LESSON

@login_required
def learn_lesson(request, lesson_id):

    lesson = Lesson.objects.get(id=lesson_id)

    course = lesson.course

    enrolled = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).exists()

    if not enrolled:

        return redirect(
            'course_detail',
            course.id
        )

    lessons = course.lessons.all()

    progress, created = Progress.objects.get_or_create(

        student=request.user,
        course=course
    )

    completed_lessons = progress.completed_lessons.all()

    context = {

        'lesson': lesson,
        'course': course,
        'lessons': lessons,
        'progress': progress,
        'completed_lessons': completed_lessons

    }

    return render(

        request,
        'learn_lesson.html',
        context
    )

def all_courses(request):

    courses = Course.objects.all()

    context = {

        'courses': courses

    }

    return render(
        request,
        'all_courses.html',
        context
    )

@login_required
def complete_lesson(request, lesson_id):

    lesson = Lesson.objects.get(id=lesson_id)

    course = lesson.course

    progress, created = Progress.objects.get_or_create(

        student=request.user,
        course=course
    )

    progress.completed_lessons.add(lesson)

    total_lessons = course.lessons.count()

    completed_count = progress.completed_lessons.count()

    percentage = int(
        (completed_count / total_lessons) * 100
    )

    progress.progress_percentage = percentage

    progress.save()

    return redirect(
        'learn_lesson',
        lesson_id=lesson.id
    )




def my_learning(request):

    progress_data = Progress.objects.filter(

        student=request.user
    )

    context = {

        'progress_data': progress_data

    }

    return render(
        request,
        'my_learning.html',
        context
    )

def course_students(request, course_id):

    course = Course.objects.get(id=course_id)

    enrollments = Enrollment.objects.filter(
        course=course
    )

    progress_data = Progress.objects.filter(
        course=course
    )

    context = {

        'course': course,
        'enrollments': enrollments,
        'progress_data': progress_data
    }

    return render(
        request,
        'course_students.html',
        context
    )


def student_dashboard(request):

    if request.user.role != "student":

        return redirect('home')

    enrolled_courses = Enrollment.objects.filter(

        student=request.user
    )

    progress_data = Progress.objects.filter(

        student=request.user
    )

    notices = Notice.objects.all().order_by(

        '-created_at'
    )

    context = {

        'enrolled_courses': enrolled_courses,

        'progress_data': progress_data,

        'notices': notices
    }

    return render(

        request,
        'student_dashboard.html',
        context
    )





def course_type_page(request, course_type):

    courses = Course.objects.filter(
        course_type=course_type
    )

    context = {

        'courses': courses,
        'course_type': course_type,
    }

    return render(
        request,
        'course_type_page.html',
        context
    )


# notice 
def create_notice(request):

    if request.user.role != "instructor":

        return redirect('home')

    if request.method == "POST":

        title = request.POST['title']

        message = request.POST['message']

        Notice.objects.create(

            instructor=request.user,

            title=title,

            message=message
        )

        return redirect('instructor_dashboard')
    


def become_teacher(request):

    return render(
        request,
        'become_teacher.html'
    )


def teacher_application(request):

    if request.method == "POST":

        TeacherRequest.objects.create(

            user=request.user,

            full_name=request.POST.get('full_name'),

            email=request.POST.get('email'),

            skills=request.POST.get('skills'),

            experience=request.POST.get('experience'),

            reason=request.POST.get('reason')

        )

        return redirect('success')

    return render(
        request,
        'become_teacher1.html'
    )


def success(request):

    return render(
        request,
        'success.html'
    )


def about(request):

    return render(
        request,
        'about.html'
    )


def contact(request):

    return render(
        request,
        'contact.html'
    )

def all_students(request):

    students = User.objects.filter(role='student')

    context = {
        'students': students
    }

    return render(request, 'all_students.html', context)