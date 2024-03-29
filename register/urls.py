from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path( '',views.index, name='home'),
    path('learner/list/', views.student_list, name='person-list'),  #ok
    path('member/list/', views.members, name='members-list'),  #ok

    path('addperson/', views.add_person, name="register_person"),  #ok
    path('student/<int:pk>', views.student, name='edit_student'), 
    path('lesson/', views.lessons, name="addlesson"),    #ok
    path('student/enrol/<int:pk>', views.enroll, name='learner_enrol'),

    path('lesson/view/<int:pk>', views.view_lessons, name="viewlesson"),
    path('lesson/view/details/<int:pk>', views.view_lesson, name="details"),
    path('lesson/summary/view', views.lesson_summary, name="lesson_summary"),

    path('attendance/<int:pk>', views.mark_attendance, name ="mark"),

    path('enrollearner/<int:pk>', views.learner_in_class, name="enrol"),

    path('person/details/<int:pk>', views.person_details, name="person_details"),
    path('edit/person/<int:pk>', views.edit_person, name="edit_person"),
    path('edit/lesson/<int:pk>', views.lesson_edit, name="edit_lesson"),
    path('online/lesson/<int:pk>', views.online_class, name="onlinelesson"),
    path('view/online/<int:pk>', views.view_video, name="videoview"),
    path('lesson/closs/<int:pk>', views.close_lesson, name="closslesson"),
    path('comment/<int:pk>', views.comment, name="comment"),
    path('join/online/<int:pk>', views.join_online, name="join_online"),
    # path('online/attendance/<int:pk>', views.online_attendance, name="online_attendance"),
    path('online/register/<int:pk>', views.register_online, name="online_register"),
    path('notice/' , views.create_notice, name= 'notice'),
    path('notice/view/' , views.notice_view, name='view'),
    path('notice/view/delete/<int:pk>', views.notice_delete, name='delete'),
    path('notice/view/update/<int:pk>', views.notice_update, name= 'update'),
    


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



admin.site.site_header= "Simani Technologies"
admin.site.site_title= "Simani Technologies"
admin.site.site_index_title = "welcome to simani technologies"
