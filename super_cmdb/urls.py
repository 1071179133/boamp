"""webssh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,re_path
from super_cmdb import views
from super_cmdb import user_views
from super_cmdb import serverhost_views
from super_cmdb import permission_views
from super_cmdb import secret_key_views

urlpatterns = [
    path('login/',views.login),
    path('welcome/',views.welcome),
    path('index/',views.index),

    ########用户管理url开始########
    path('user_list/',user_views.user_list_info),
    path('user_info/',user_views.user_info),
    path('user_add/',user_views.user_add),
    re_path('user_edit-(?P<user_id>\d+)/',user_views.user_edit),
    path('user_del/',user_views.user_del),
    ########用户管理url结束########

    ########机器管理url开始########
    path('serverhost_list/',serverhost_views.serverhost_list),
    path('serverhost_add/',serverhost_views.serverhost_add),
    path('serverhost_del/',serverhost_views.serverhost_del),
    re_path('serverhost_edit-(?P<host_id>\d+)/',serverhost_views.serverhost_edit),
    ########机器管理url结束########

    ########密钥管理url开始########
    path('secret_key/',secret_key_views.secret_key),
    path('secret_key_add/',secret_key_views.secret_key_add),
    re_path('secret_key_edit-(?P<secret_key_id>\d+)/',secret_key_views.secret_key_edit),
    ########密钥管理url结束########

    ########项目管理url开始########
    path('project_list/',permission_views.project_list),
    path('project_add/',permission_views.project_add),
    re_path('project_edit-(?P<project_id>\d+)/', permission_views.project_edit),
    path('project_del/',permission_views.project_del),
    ########项目管理url结束########

    ########权限配置url开始########
    path('permission_set/', permission_views.permission_set),
    ########权限配置url结束########

    ########安装agent url开始########
    path('install_agent/', views.install_agent),
    re_path('install_agent_host_(?P<project_id>\d+)/', views.install_agent_host,name="install_agent_host"),
    ########安装agent url结束########


    path('icon/',views.icon),
    path('dev_record/',views.dev_record),
    path('dev_record_add/',views.dev_record_add),

]
