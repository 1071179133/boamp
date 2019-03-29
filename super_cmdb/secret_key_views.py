from django.shortcuts import render,redirect,HttpResponse
from databases_models import models
from utils.auth_manog import auth_manog_done
import base64,re
from django.http import JsonResponse
from utils.access_restriction import access_rt


@auth_manog_done
def secret_key(request):
    if request.method == "GET":
        user_id = request.session.get("user_id")
        secret_key_list = models.SecretKey.objects.filter(user_id=user_id).all()
        return render(request, 'super_cmdb/secret_key_list.html', {"secret_key_list":secret_key_list})

@auth_manog_done
def secret_key_add(request):
    if request.method == "GET":
        auth_type_list = models.MyAuthType.objects.all()
        return render(request,'super_cmdb/secret_key_add.html',{"auth_type_list":auth_type_list})
    if request.method == "POST":
        rsg = {'status': 0, 'message': None, 'error': None}
        user_id = request.session.get("user_id")
        login_user = request.POST.get("login_user")
        auth_type_id = request.POST.get("auth_type_id")
        key = request.POST.get("key")
        #key_password = request.POST.get("key_password")    #弃用密码，改为手动填写
        try:
            #key_password = base64.b64encode(bytes(key_password, encoding="utf8"))
            #key_password = str(key_password, encoding="utf-8")
            models.SecretKey.objects.create(login_user=login_user,auth_type_id=auth_type_id,key=key,user_id=user_id)
        except Exception as e:
            print(e)
            rsg["status"] = 1
            rsg['error':] = e
        return JsonResponse(rsg)

@auth_manog_done
def secret_key_edit(request,secret_key_id):
    if request.method == "GET":
        secret_key_info = models.SecretKey.objects.filter(id=secret_key_id).first()
        auth_type_list = models.MyAuthType.objects.all()
        return render(request,'super_cmdb/secret_key_edit.html',{"secret_key_info":secret_key_info,"auth_type_list":auth_type_list})
    if request.method == "POST":
        rsg = {'status': 0, 'message': None, 'error': None}
        login_user = request.POST.get("login_user")
        auth_type_id = request.POST.get("auth_type_id")
        key = request.POST.get("key")
        #key_password = request.POST.get("key_password")
        try:
            #key_password = base64.b64encode(bytes(key_password, encoding="utf8"))
            #key_password = str(key_password, encoding="utf-8")
            #models.SecretKey.objects.filter(id=secret_key_id).update(login_user=login_user,auth_type_id=auth_type_id,key=key,key_password=key_password)
            obj = models.SecretKey.objects.get(id=secret_key_id)
            obj.login_user = login_user
            obj.auth_type_id = auth_type_id
            obj.key = key
            #obj.key_password = key_password
            obj.save()
        except Exception as e:
            print(e)
            rsg["status"] = 1
            rsg['error':] = e
        return JsonResponse(rsg)