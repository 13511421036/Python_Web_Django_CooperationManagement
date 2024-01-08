# coding=utf-8

from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello, name='hello'),
    path('add_worker/', views.add_worker, name='add_worker'),
    path('edit_worker/', views.edit_worker, name='edit_worker'),
    path('delete_worker/', views.delete_worker, name='delete_worker'),
    path('add_task/', views.add_task, name='add_task'),
    path('administrator_login/', views.administrator_login, name='administrator_login'),
    path('administrator_main/', views.administrator_login, name='administrator_main'),
    path('add_group/', views.add_group, name='add_group'),
    path('create_administrator/', views.create_administrator, name='create_administrator'),
    path('worker_main/', views.worker_login, name='worker_main'),
    path('worker_login/', views.worker_login, name='worker_login'),
    path('delete_task/', views.delete_task, name='delete_task'),
    path('delete_group/', views.delete_group, name='delete_group'),
    path('edit_task/', views.edit_task, name='edit_task'),
    path('edit_group/', views.edit_group, name='edit_group'),
    path('view_group/', views.view_group, name='view_group'),
    path('view_task/', views.view_task, name='view_task'),
    path('add_worker_group/', views.add_worker_group, name='add_worker_group'),
    path('add_worker_task/', views.add_worker_task, name='add_worker_task'),
    path('edit_administrator/', views.edit_administrator, name='edit_administrator'),
    path('delete_administrator/', views.delete_administrator, name='delete_administrator'),
    path('back_to_vip_administrator/', views.back_to_vip_administrator, name='back_to_vip_administrator'),
    path('back_to_administrator_main/', views.back_to_administrator_main, name='back_to_administrator_main'),
]

