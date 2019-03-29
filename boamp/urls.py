
from django.contrib import admin
from django.urls import path,re_path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webssh/',include('webssh.urls')),
    path('super_cmdb/',include('super_cmdb.urls')),
    path('super_admin/',include('super_admin.urls')),
    path('super_monitor/',include('super_monitor.urls')),
]
