from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='registration/login.html',redirect_authenticated_user=True), name='home'),
    path('register/', views.register, name="register"),
    path('', views.home, name='home'),
    path('edit_profile/', views.updatemember, name='update_profile'),
    path('profile/', views.profile, name='profile'),
    path('chat/<str:username>', views.chat, name='chat'),
    path('chats/', views.chat_list, name='chat_list'),
    path('search/', views.search_user, name='search_user')
    
]
