"""
URL configuration for catechesm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from user import views as user_views
from user.forms import MyPasswordResetForm,MyPasswordChangeForm,MySetPasswordForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("register.urls")),


    path('category/<int:pk>/tracer',user_views.category, name='category' ),
    path('mode/<int:pk>/tracer',user_views.mode, name='mode' ),
    path('level/<int:pk>/tracer',user_views.level, name='level' ),
    path('online/myname/<int:pk>/search_name',user_views.search_name, name='my_name'),
    path('normal/myname/<int:pk>/search_name_for/normal',user_views.search_name_normal, name='normal'),
    path('online/verify/<int:pk>',user_views.verify_online, name='verify_online' ),
    path('self/registration/',user_views.self_registration, name='self-register' ),

    path('tracer/delete/<int:pk>/tracer',user_views.delete_tracer, name='tracer_delete' ),

    path('register/',user_views.register, name='register' ),
    path('accounts/profile/',user_views.userprofile, name='userprofile' ),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='user/login.html'), name="login"),
    path('logout/',auth_views.LogoutView.as_view(template_name='user/logout.html'), name="logout"),
    path('messages/send/<int:pk>/', user_views.send_message, name='send_message'),






    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='user/changepassword.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone'),name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='user/changepassworddone.html' ),name='passwordchangedone'),
    path('logout/', auth_views.LogoutView.as_view(next_page ='login'), name='logout'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html', form_class= MyPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header= "Simani Technologies"
admin.site.site_title= "Simani Technologies"
admin.site.site_index_title = "welcome to simani technologies"
