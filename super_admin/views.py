from django.shortcuts import render,redirect
from super_admin import super_admin
import importlib
from django.core.paginator import Paginator
from super_admin.utils import table_filter,table_sort,table_search
from django.http import JsonResponse
from super_admin.forms import create_model_form
from utils.auth_manog import auth_manog_done

# Create your views here.

@auth_manog_done
def index(request):
    return render(request,"super_admin/table_index.html",{"table_list":super_admin.enabled_admins})

@auth_manog_done
def display_table_obj(request,app_name,table_name):
    admin_class = super_admin.enabled_admins[app_name][table_name]
    table_name_zh = admin_class.model._meta.verbose_name_plural

    #获取数据
    #query_sets = admin_class.model.objects.get_queryset().order_by('-id')
    query_sets,filter_conditions = table_filter(request,admin_class)    #过滤后的结果，filter_conditions 在utils中生成，是一个字典
    #模糊查询
    query_sets = table_search(request,admin_class,query_sets)
    query_sets,orderby_key = table_sort(request,admin_class,query_sets)     #排序
    #分页
    pg_number = request.session.get("pg_number")
    if not pg_number:
        pg_number = 30
    paginator = Paginator(query_sets, pg_number)  # admin_class.list_per_page ： 每页显示多少条数据,在king_admin.py的list_per_page定义
    page = request.GET.get('page')
    query_sets = paginator.get_page(page)

    return render(request,"super_admin/table_objs.html",{
        "admin_class":admin_class,
        "query_sets":query_sets,
        "filter_conditions":filter_conditions,
        "orderby_key":orderby_key,
        "previous_orderby":request.GET.get("o",""), #如果获取不到值，则为空
        "search_text":request.GET.get('_q',''),     #返回搜索的内容让搜索页面显示搜索操作的内容
        "table_name_zh":table_name_zh
    })

@auth_manog_done
def pg_num(request):
    """设定每页显示多少条数据"""
    if request.method == "POST":
        pg_number = request.POST.get("pg_number",30)
        request.session["pg_number"] = pg_number
        return JsonResponse({"code":0,"msg":"ok"})

@auth_manog_done
def table_obj_add(request,app_name,table_name):
    """添加数据"""
    admin_class = super_admin.enabled_admins[app_name][table_name]
    model_form_class = create_model_form(request, admin_class)

    if request.method == "POST":
        form_obj = model_form_class(request.POST)               #这是创建
        if form_obj.is_valid(): #如果提交数据合法则保存
            form_obj.save()
            return redirect(request.path.replace("/add",""))
    else:
        form_obj = model_form_class()   #instance在model_form中默认为空，把obj数据传给model_form，model_form就会在前端展示页展示obj数据
    return render(request,"super_admin/table_obj_add.html",{
        "form_obj":form_obj,
        "app_name": app_name,
        "admin_class": admin_class,
    })


@auth_manog_done
def table_obj_change(request,app_name,table_name,obj_id):
    """编辑数据"""
    admin_class = super_admin.enabled_admins[app_name][table_name]
    model_form_class = create_model_form(request,admin_class)
    obj = admin_class.model.objects.get(id=obj_id)

    if request.method == "POST":
        #form_obj = model_form_class(request.POST)               #这是创建
        form_obj = model_form_class(request.POST,instance=obj)  #这是更新
        if form_obj.is_valid(): #如果提交数据合法则保存
            form_obj.save()
            replace_url = "/%s/change"%obj_id
            return redirect(request.path.replace(replace_url, ""))
    else:
        form_obj = model_form_class(instance=obj)   #instance在model_form中默认为空，把obj数据传给model_form，model_form就会在前端展示页展示obj数据
    return render(request,"super_admin/table_obj_change.html",{
        "form_obj":form_obj,
        "app_name":app_name,
        "table_name":table_name,
        "admin_class": admin_class,
        "obj_id": obj_id,
    })

@auth_manog_done
def table_obj_delete(request,app_name,table_name,obj_id):
    """删除数据"""
    admin_class = super_admin.enabled_admins[app_name][table_name]
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == "GET":
        return render(request,"super_admin/table_obj_delete.html",{
            "obj":obj,
            "admin_class":admin_class,
            "app_name": app_name,
        })
    elif request.method == "POST":
        obj.delete()
        return redirect("/super_admin/%s/%s/" %(app_name,table_name))



