from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('addperson/', views.add_person),
    path('student/', views.student),
    path('lesson/', views.lessons),
    path('lesson/view', views.view_lessons),
    path('lesson/view/<int:pk>', views.view_lesson),
    path('lesson/attendance/', views.View_attendance, name='view_attendance'),
    path('attendance/<int:pk>', views.mark_attendance),
    path('attendance/', views.attendance_summary),


]
