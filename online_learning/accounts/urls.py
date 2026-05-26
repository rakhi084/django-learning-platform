from django.urls import path
from .views import *

urlpatterns = [

    path('', home, name='home'),

    path('register/', register_view, name='register'),

    path('login/', login_view, name='login'),

    path('logout/', logout_view, name='logout'),
     path(
        'instructor-dashboard/',
        instructor_dashboard,
        name='instructor_dashboard'
    ),

    path(
        'create-course/',
        create_course,
        name='create_course'
    ),
    path(
    'course/<int:course_id>/',
    course_detail,
    name='course_detail'
),

path(
    'course/<int:course_id>/add-lesson/',
    add_lesson,
    name='add_lesson'
),

path(
    'course/<int:course_id>/enroll/',
    enroll_course,
    name='enroll_course'
),

path(
    'lesson/<int:lesson_id>/',
    learn_lesson,
    name='learn_lesson'
),

path(
    'courses/',
    all_courses,
    name='all_courses'
),
path(
    'complete-lesson/<int:lesson_id>/',
    complete_lesson,
    name='complete_lesson'
),
path(
    'my-learning/',
    my_learning,
    name='my_learning'
),
path(
    'course/<int:course_id>/students/',
    course_students,
    name='course_students'
),
path(
    'student-dashboard/',
    student_dashboard,
    name='student_dashboard'
),
path(
    'courses/<str:course_type>/',
    course_type_page,
    name='course_type'
),
path(
    'create-notice/',
    create_notice,
    name='create_notice'
),
path(
    'become-teacher/',
    become_teacher,
    name='become_teacher'
),

path(
    'teacher-application/',
    teacher_application,
    name='teacher_application'
),

path(
    'success/',
    success,
    name='success'
),
path(
    'about/',
    about,
    name='about'
),

path(
    'contact/',
    contact,
    name='contact'
),
 path('all-students/', all_students, name='all_students'),

]