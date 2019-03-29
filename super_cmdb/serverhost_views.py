from django.shortcuts import render,redirect,HttpResponse
from databases_models import models
from utils.auth_manog import auth_manog_done
from utils import pagination
import re

# Create your views here.

#######################遗留一个问题：
    #当新增加一个用户时，怎么让新用户与已有机器关联
    #尝试思路：
        # 1.新增用户后，在权限配置那给用户相应的项目权限：user_project表，通过用户名查到用户拥有的项目，多对多查询
        # 2.循化项目列表，提取一个旧用户为条件查询serverhost_user表得到拥有的机器id列表[此步不准确，万一提取到新用户id作为查询条件呢]
        # 3.再循环拥有的机器id列表，把新用户id与机器id插入到serverhost_user，完成关联
    #解决方法：
        #查看super_cmdb/views.py的permission_set函数

@auth_manog_done
def serverhost_list(request):
    if request.method == "GET":
        user_id = request.session.get("user_id")
        user_obj = models.User.objects.filter(id=user_id).first()
        host_list = user_obj.serverhost_set.all()
        host_num = host_list.count()
        """
        反向查询：xxxx_set  xxxx:表名
		 v = models.UserGroup.objects.filter(uid=1).first()
        for user in v.userinfo_set.all():
            print(user.username)
       """
    elif request.method == "POST":
        host_list = []
        host_num = []
        project = request.POST.get("project")
        try:
            project_obj = models.Project.objects.get(name=project)
            host_list = project_obj.serverhost_set.all()
            host_num = host_list.count()
        except Exception as e:
            print(e)

    current_page = int(request.GET.get("Page", 1))  # 获取用户get请求的页码数
    select_current_page = int(request.COOKIES.get("per_page_count", 13))  # 获取当前页面cookie记录的显示条数,默认是10
    # select_current_page=10
    page_obj = pagination.Page(current_page, len(host_list),select_current_page)  # 创建page_obj对象  per_page_count=10,page_num=7是变量，可改动
    host_list = host_list[page_obj.start_count:page_obj.end_count]  # 每页显示数据条数列表
    page_list = page_obj.page_str("super_cmdb/serverhost_list/")  # 分页的所有内容

    return render(request, 'super_cmdb/serverhost_list.html',{"host_list":host_list,"page_list":page_list,"host_num":host_num})


@auth_manog_done
def serverhost_add(request):
    user_id = request.session.get("user_id")
    if request.method == "GET":
        user_id = request.session.get("user_id")
        user_obj = models.User.objects.filter(id=user_id).first()
        my_project_list = user_obj.project.all()
        return render(request,"super_cmdb/serverhost_add.html",{"my_project_list":my_project_list})
    elif request.method == "POST":
        rsg = {'status': 0, 'message': None, 'error': None}
        host_name = request.POST.get("host_name")
        host_ip = request.POST.get("host_ip")
        host_port = request.POST.get("host_port")
        project_id = request.POST.get("project_id")
        if not models.ServerHost.objects.filter(host_ip=host_ip):
            try:
                models.ServerHost.objects.create(host_name=host_name, host_ip=host_ip, host_port=host_port,project_id=project_id)
                ###多对多操作：增加数据   开始### 机器与用户是多对多关联的，当添加机器时，把拥有该项目权限的用户与机器关联，使得拥有该项目权限的其他用户也可以看到新增的机器列表
                host_obj = models.ServerHost.objects.get(host_ip=host_ip)
                project_obj = models.Project.objects.filter(id=project_id).first()
                user_obj = project_obj.user_set.all()
                host_obj.user.add(*user_obj)    #一台机器关联多个用户
                ###多对多操作：增加数据   结束###
            except Exception as e:
                print("添加机器%s失败"%host_ip,e)
                log_fail = "添加用户【%s】失败" % host_ip
                return HttpResponse("not done")
            else:
                log_success = "添加机器【%s】成功"%host_ip
                return HttpResponse("增加成功")
        else:
            print(host_ip,"已存在")
            msg = host_ip + "已存在"
            #return render(request,"dev_record_add.html",{"msg":msg})
            return HttpResponse(msg)

@auth_manog_done
def serverhost_edit(request,host_id):
    if request.method == "GET":
        user_id = request.session.get("user_id")
        user_obj = models.User.objects.filter(id=user_id).first()
        my_project_list = user_obj.project.all()
        host_info = models.ServerHost.objects.filter(id=host_id).first()
        return render(request,"super_cmdb/serverhost_edit.html",{"host_info":host_info,"my_project_list":my_project_list})
    elif request.method == "POST":
        host_name = request.POST.get("host_name")
        host_ip = request.POST.get("host_ip")
        host_port = request.POST.get("host_port")
        project_id = request.POST.get("project_id")
        try:
            #models.ServerHost.objects.filter(id=host_id).update(host_name=host_name,host_ip=host_ip,host_port=host_port,project_id=project_id)
            obj = models.ServerHost.objects.get(id=host_id)
            obj.host_name = host_name
            obj.host_ip = host_ip
            obj.host_port = host_port
            obj.project_id = project_id
            obj.save()
            log_success = "编辑主机【%s】成功" % host_ip
        except Exception as e:
            log_success = "编辑主机【%s】失败：%s" % (host_ip,e)
            print(log_success)
        return HttpResponse("OK")

@auth_manog_done
def serverhost_del(request):
    if request.method == "POST":
        host_id = request.POST.get("host_id")   #前端传过来的全是字符串
        nums = re.findall(r'\d+', host_id)      #匹配user_id组成数组
        if isinstance(nums,list):    #判断user_id是不是一个list
            for id in nums:
                #id = int(id)
                host_ip = models.ServerHost.objects.filter(id=id).first().host_ip
                models.ServerHost.objects.filter(id=id).delete()
                log_success = "删除机器【%s】成功" % host_ip
                print(log_success)
        return redirect("/super_cmdb/serverhost_list/")