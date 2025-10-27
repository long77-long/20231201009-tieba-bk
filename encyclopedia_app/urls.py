from django.urls import path
from . import views

urlpatterns = [
    path('', views.entry_list, name='entry_list'),
    path('<str:title>/', views.entry_detail, name='entry_detail'),
    path('create/', views.entry_create, name='entry_create'),
    path('<str:title>/edit/', views.entry_edit, name='entry_edit'),
]