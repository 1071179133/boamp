from django.contrib import admin
from django.urls import path,re_path
from super_admin import views

urlpatterns = [
    path('index/', views.index,name="table_index"),
    re_path('(?P<app_name>\w+)/(?P<table_name>\w+)/add/', views.table_obj_add,name="table_objs_add"),
    re_path('(?P<app_name>\w+)/(?P<table_name>\w+)/(?P<obj_id>\d+)/change/', views.table_obj_change,name="table_objs_change"),
    re_path('(?P<app_name>\w+)/(?P<table_name>\w+)/(?P<obj_id>\d+)/delete/', views.table_obj_delete,name="obj_delete"),
    re_path('(\w+)/(\w+)/', views.display_table_obj,name="table_objs"),
    path('pg_num/',views.pg_num,name="pg_num"),
]
