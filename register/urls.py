from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('addperson/', views.add_person, name="register_person"),
    path('student/<int:pk>', views.student, name='edit_student'),
    path('lesson/', views.lessons, name="addlesson"),
    path('student/enrol/<int:pk>', views.enroll, name='learner_enrol'),

    path('lesson/view', views.view_lessons, name="viewlesson"),
    path('lesson/view/<int:pk>', views.view_lesson, name="details"),
    # path('lesson/attendance/<int:pk>', views.View_attendance, name='view_attendance'),
    path('attendance/<int:pk>', views.mark_attendance, name ="mark"),
    path('attendance/', views.attendance_summary),

    path('enrollearner/<int:pk>', views.learner_in_class, name="enrol"),
    path('person/details/<int:pk>', views.person_details, name="person_details"),
    path('edit/person/<int:pk>', views.edit_person, name="edit_person"),
    path('edit/lesson/<int:pk>', views.lesson_edit, name="edit_lesson"),
    path('online/lesson/<int:pk>', views.onlineclass, name="onlinelesson"),
    path('view/online/<int:pk>', views.view_video, name="videoview"),
    path('report/', views.report, name="report"),
    path('lesson/closs/<int:pk>', views.close_lesson, name="closslesson"),
    path('comment/<int:pk>', views.comment, name="comment"),
    path('join/online/<int:pk>', views.join_online, name="join_online"),
    # path('online/attendance/<int:pk>', views.online_attendance, name="online_attendance"),
    path('online/register/<int:pk>', views.register_online, name="online_register"),











]
