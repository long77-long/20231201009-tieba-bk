from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('encyclopedia_app.urls')),  # 将主应用设为根路径
    path('users/', include('encyclopedia_app.urls')),  # 用户相关路由
]