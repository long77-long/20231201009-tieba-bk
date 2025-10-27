from django.urls import path
from . import views

urlpatterns = [
    # 首页和帖子相关路由
    path('', views.home, name='home'),
    path('detail/<str:title>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('edit/<str:title>/', views.post_edit, name='post_edit'),
    
    # 用户相关路由
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    
    # 贴吧相关路由
    path('tieba/<str:tieba_name>/', views.tieba_detail, name='tieba_detail'),
]