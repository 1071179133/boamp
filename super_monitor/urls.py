
from django.contrib import admin
from django.urls import path,re_path
from super_monitor import views
urlpatterns = [
    path('monitor_api/',views.monitor_api),
    path('monitor_list/',views.monitor_list),
    path('monitor_history/', views.monitor_history),
]
