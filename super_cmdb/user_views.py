from django.shortcuts import render,redirect,HttpResponse
from databases_models import models
from utils.auth_manog import auth_manog_done
from utils import pagination
from utils.hashlib_done import encryption
from utils.access_restriction import access_rt
import re
from boamp.settings import logger

permission_status = "permission denied"

# Create your views here.
@auth_manog_done
def user_list_info(request):
    if access_rt(request,models) == permission_status:#判断是否有权限访问函数
        return HttpResponse(permission_status)
    else:
        logger.info("访问用户列表")
        user_list = models.User.objects.all()
        user_all_num = user_list.count()
        current_page = int(request.GET.get("Page", 1))  # 获取用户get请求的页码数
        select_current_page = int(request.COOKIES.get("per_page_count", 13))  # 获取当前页面cookie记录的显示条数,默认是10
        # select_current_page=10
        page_obj = pagination.Page(current_page, len(user_list),
                                   select_current_page)  # 创建page_obj对象  per_page_count=10,page_num=7是变量，可改动
        user_list = user_list[page_obj.start_count:page_obj.end_count]  # 每页显示数据条数列表
        page_list = page_obj.page_str("super_cmdb/user_list/")  # 分页的所有内容
        return render(request, "super_cmdb/user_list.html",
                      {"user_list": user_list, "page_list": page_list, "user_all_num": user_all_num})

@auth_manog_done
def user_info(request):
    user_id = request.session.get("user_id")
    user_info = models.User.objects.filter(id=user_id).first()
    has_project_list = user_info.project.all()
    return render(request,"super_cmdb/user_info.html",{"user_info":user_info,"has_project_list":has_project_list})

@auth_manog_done
def user_add(request):
    if access_rt(request,models) == permission_status:#判断是否有权限访问函数
        return HttpResponse(permission_status)
    else:
        if request.method == "GET":
            user_type_list = models.UserType.objects.all()
            return render(request,"super_cmdb/user-add.html",{"user_type_list":user_type_list})
        elif request.method == "POST":
            rsg = {'status': 0, 'message': None, 'error': None}
            user = request.POST.get("user")
            password = request.POST.get("password")
            password = encryption(password)     #加密密码
            usertype_id = request.POST.get("usertype_id")
            if not models.User.objects.filter(name=user):
                try:
                    models.User.objects.create(name=user, password=password, usertype_id=usertype_id)
                except Exception as e:
                    print("添加用户%s失败"%user,e)
                    log_fail = "添加用户【%s】失败" % user
                    return HttpResponse("not done")
                else:
                    log_success = "添加用户【%s】成功"%user
                    return HttpResponse("增加成功")
            else:
                print(user,"已存在")
                msg = user + "已存在"
                #return render(request,"dev_record_add.html",{"msg":msg})
                return HttpResponse(msg)

@auth_manog_done
def user_edit(request,user_id):
    if request.method == "GET":
        user_info = models.User.objects.filter(id=user_id).first()
        #user_type_list = models.UserType.objects.all()
        return render(request,"super_cmdb/user-edit.html",{"user_info":user_info})
    elif request.method == "POST":
        old_password = models.User.objects.get(id=user_id).password
        name = request.POST.get("user")
        password = request.POST.get("password")
        if old_password == password:
            pass
        else:
            password = encryption(password)  # 加密密码
        print(password)
        phone = request.POST.get("phone")
        phone_bak = request.POST.get("phone_bak")
        motto = request.POST.get("motto")
        hobby = request.POST.get("hobby")
        try:
            #models.User.objects.filter(id=user_id).update(name=name,password=password,phone=phone,phone_bak=phone_bak,motto=motto,hobby=hobby)
            obj = models.User.objects.get(id=user_id)
            obj.name = name
            obj.password = password
            obj.phone = phone
            obj.phone_bak = phone_bak
            obj.motto = motto
            obj.hobby = hobby
            obj.save()
        except Exception as e:
            print(e)
        log_success = "编辑用户【%s】成功" % name
        return HttpResponse("OK")

@auth_manog_done
def user_del(request):
    if access_rt(request,models) == permission_status:#判断是否有权限访问函数
        return HttpResponse(permission_status)
    else:
        if request.method == "POST":
            user_id = request.POST.get("user_id")   #前端传过来的全是字符串
            nums = re.findall(r'\d+', user_id)      #匹配user_id组成数组
            if isinstance(nums,list):    #判断user_id是不是一个list
                for id in nums:
                    #id = int(id)
                    user_name = models.User.objects.filter(id=id).first().name
                    models.User.objects.filter(id=id).delete()
                    log_success = "删除用户【%s】成功" % user_name
                    print(log_success)
            return redirect("/super_cmdb/user_list/")