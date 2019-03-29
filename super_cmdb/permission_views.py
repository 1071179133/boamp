import re
from django.shortcuts import render,redirect,HttpResponse
from databases_models import models
from utils.auth_manog import auth_manog_done
from utils.access_restriction import access_rt

permission_status = "permission denied"

@auth_manog_done
def project_list(request):
    """项目列表"""
    if access_rt(request,models) == permission_status:#判断是否有权限访问函数
        return HttpResponse(permission_status)
    else:
        projects = models.Project.objects.all()
        return render(request,'super_cmdb/project_list.html',{"projects":projects})

@auth_manog_done
def project_add(request):
    """项目添加"""
    if access_rt(request,models) == permission_status:#判断是否有权限访问函数
        return HttpResponse(permission_status)
    else:
        if request.method == "GET":
            return render(request,'super_cmdb/project_add.html')
        if request.method == "POST":
            name = request.POST.get("name")
            describe = request.POST.get("describe")
            try:
                models.Project.objects.create(name=name,describe=describe)
                return HttpResponse('ok')
            except Exception as e:
                print(e)
                return HttpResponse("faild")

@auth_manog_done
def project_edit(request,project_id):
    """项目编辑"""
    if access_rt(request,models) == permission_status:#判断是否有权限访问函数
        return HttpResponse(permission_status)
    else:
        if request.method == "GET":
            project_info = models.Project.objects.filter(id=project_id).first()
            return render(request,"super_cmdb/project_edit.html",{"project_info":project_info})
        if request.method == "POST":
            name = request.POST.get("name")
            describe = request.POST.get("describe")
            try:
                obj = models.Project.objects.get(id=project_id)
                obj.name = name
                obj.describe = describe
                obj.save()
                return HttpResponse('ok')
            except Exception as e:
                print(e)
                return HttpResponse("faild")

@auth_manog_done
def project_del(request):
    """项目删除"""
    if access_rt(request,models) == permission_status:#判断是否有权限访问函数
        return HttpResponse(permission_status)
    else:
        if request.method == "POST":
            project_id = request.POST.get("project_id")   #前端传过来的全是字符串
            nums = re.findall(r'\d+', project_id)      #匹配user_id组成数组
            if isinstance(nums,list):    #判断user_id是不是一个list
                for id in nums:
                    #id = int(id)
                    name = models.Project.objects.filter(id=id).first().name
                    models.Project.objects.filter(id=id).delete()
                    log_success = "删除用户【%s】成功" % name
                    print(log_success)
            return redirect("/super_cmdb/project_list/")

@auth_manog_done
def permission_set(request):
    """配置权限"""
    if access_rt(request,models) == permission_status:#判断是否有权限访问函数
        return HttpResponse(permission_status)
    else:
        if request.method == "GET":
            user_list = models.User.objects.all()
            project_list = models.Project.objects.all()
            return render(request,"super_cmdb/permission_set.html",{"user_list":user_list,"project_list":project_list})
        if request.method == "POST":
            status = request.POST.get("status")
            user_id = request.POST.get("user_id")
            project_id = request.POST.get("project_id")
            try:
                user_obj = models.User.objects.get(id=user_id)
                project_obj = models.Project.objects.get(id=project_id)
                host_obj = project_obj.serverhost_set.all()
                if status == "setting":
                    ###多对多操作：增加数据   开始### 用户与项目是多对多关联的，当配置时，把用户与项目关联
                    user_obj.project.add(project_obj)
                    #用户关联属于项目id的所有机器
                    user_obj.serverhost_set.add(*host_obj)    #一个用户关联多台机器
                    print("用户id:%s关联属于项目id：%s的所有机器成功"%(user_id,project_id))
                    ###多对多操作：增加数据   结束###
                else:
                    ###多对多操作：删除数据   开始### 用户与项目删除关联
                    user_obj.project.remove(project_obj)
                    # 删除用户关联属于项目id的所有机器
                    user_obj.serverhost_set.remove(*host_obj)
                    print("删除用户id:%s关联属于项目id：%s的所有机器成功"%(user_id,project_id))
                    ###多对多操作：增加数据   结束###
                return HttpResponse("ok")
            except Exception as e:
                print(e)
                return HttpResponse("faild")