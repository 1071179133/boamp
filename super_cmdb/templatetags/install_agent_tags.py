from django import template
from django.utils.safestring import mark_safe
register = template.Library()	#创建register对象，register名字不能改
from databases_models import models

@register.simple_tag		#使用装饰器
def get_project_id(project_id):
    return project_id

@register.simple_tag		#使用装饰器
def get_project_hosts(project_id):	#参数自定义
    #操作逻辑......
    project_obj = models.Project.objects.get(id=project_id)
    host_list = project_obj.serverhost_set.all()
    return host_list