from django.shortcuts import render,redirect,HttpResponse
from databases_models import models
from utils.auth_manog import auth_manog_done
from utils.hashlib_done import encryption
from django.http import JsonResponse
from boamp.settings import BASE_DIR
from utils import my_paramiko_ssh
import os

# Create your views here.
#创建初始账号密码
name = "root"
password = "super_boamp"
password = encryption(password) #加密密码
if not models.User.objects.filter(name=name).first():
    models.UserType.objects.create(id=1,name="超级管理员")
    models.UserType.objects.create(id=2,name="管理员")
    models.User.objects.create(name=name, password=password, usertype_id=1)


def login(request):
    if request.method == "GET":
        request.session.set_expiry(0.1) #当访问登陆页面时，使当前的session失效，避免无验证也能根据历史session成功登陆
        return render(request, "super_cmdb/login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password = encryption(password) #加密密码
        user_info = models.User.objects.filter(name=username,password=password).first()
        if user_info:
            #print(username,password)
            request.session["user_id"] = user_info.id
            request.session["username"] = username
            request.session["is_login"] = True
            request.session.set_expiry(3600)   #与setting中的SESSION_SAVE_EVERY_REQUREST = True配合，不访问1小时后自动退出账号
            return redirect("/super_cmdb/index")
        else:
            #return render(request, "super_cmdb/login.html")
            status = {"code":1,"msg":"登陆失败,请检查账号密码"}
            return JsonResponse(status)

@auth_manog_done
def welcome(request):
    user_list = models.User.objects.all()
    host_list = models.ServerHost.objects.all()
    return render(request,'super_cmdb/welcome.html',{"user_list":user_list,"host_list":host_list})

@auth_manog_done
def index(request):
    return render(request,'super_cmdb/index.html')

@auth_manog_done
def icon(request):
    return render(request,'super_cmdb/unicode.html')

@auth_manog_done
def dev_record(request):
    if request.method == "GET":
        dev_record_list = models.DevRecord.objects.all().order_by("-create_time")
        return render(request, 'super_cmdb/dev_record.html',{"dev_record_list":dev_record_list})

@auth_manog_done
def dev_record_add(request):
    if request.method == "GET":
        return render(request, 'super_cmdb/dev_record_add.html')
    elif request.method == "POST":
        name = request.POST.get("name")
        content = request.POST.get("content")
        try:
            models.DevRecord.objects.create(name=name,content=content)
            return HttpResponse("ok")
        except Exception as e:
            print(e)
            return HttpResponse("not ok")

@auth_manog_done
def install_agent(request):
    if request.method == "GET":
        user_id = request.session.get("user_id")
        user_obj = models.User.objects.filter(id=user_id).first()
        my_project_list = user_obj.project.all()
        return  render(request, "super_cmdb/install_agent_select_project.html", {"my_project_list":my_project_list})

@auth_manog_done
def install_agent_host(request,project_id):
    if request.method == "GET":
        auth_type_list = models.MyAuthType.objects.all()
        project_obj = models.Project.objects.get(id=project_id)
        host_list = project_obj.serverhost_set.all()
        auth_type_list = models.MyAuthType.objects.all()
        return render(request, "super_cmdb/install_agent_select_host.html",{"host_list":host_list,"auth_type_list":auth_type_list})
    elif request.method == "POST":
        user_id = request.session.get("user_id")

        host_ip = request.POST.get("host_ip")
        host_port = int(request.POST.get("host_port"))
        auth_type = request.POST.get("auth_type")
        login_user = request.POST.get("login_user")
        password = request.POST.get("password")
        #print(host_ip,host_port,auth_type,login_user,password)
        agent_file_dir = os.path.join(BASE_DIR,"super_cmdb/agent_file/")
        if not os.path.exists(agent_file_dir):
            os.makedirs(agent_file_dir)
        agent_filename = os.path.join(agent_file_dir,"super_monitor_agent.py")
        target_filename = "/tmp/super_monitor_agent.py"
        cmd_list = [
            "mkdir -p /data/super_monitor_agent/ && mv /tmp/super_monitor_agent.py /data/super_monitor_agent/",
            "nohup python /data/super_monitor_agent/super_monitor_agent.py > /dev/null 2>&1 &"
        ]
        if auth_type == "key":
            secret_key_info = models.SecretKey.objects.filter(user=user_id, auth_type=1).first()
            pkey_file_str = secret_key_info.key
            Identity_filename = os.path.join(BASE_DIR, "super_cmdb/agent_file/Identity_temp")
            try:
                with open(Identity_filename,'w') as f:
                    f.write(pkey_file_str)
                my_paramiko_ssh.paramiko_scp(host_ip,host_port,password,login_user,agent_filename,target_filename,pkey_file=Identity_filename)
                for cmd in cmd_list:
                    result = my_paramiko_ssh.paramiko_ssh(host_ip,host_port,password,login_user,cmd,pkey_file=Identity_filename)
                os.remove(Identity_filename)
                if result[0] == 0:
                    ret = {"status": "ok", "message": "通过密钥远程安装agent成功"}
                else:
                    ret = {"status": "faild", "message": "通过密钥远程安装agent失败:%s"%result[1]}
            except Exception as e:
                ret = {"status": "faild", "message": "通过密钥远程安装agent失败%s"%e}
                print(e)
        elif auth_type == "password":
            try:
                my_paramiko_ssh.paramiko_scp(host_ip, host_port, password, login_user, agent_filename, target_filename,pkey_file=None)
                for cmd in cmd_list:
                    result = my_paramiko_ssh.paramiko_ssh(host_ip, host_port, password, login_user, cmd, pkey_file=None)
                if result[0] == 0:
                    ret = {"status": "ok", "message": "通过密钥远程安装agent成功"}
                else:
                    ret = {"status": "faild", "message": "通过密钥远程安装agent失败:%s"%result[1]}
            except Exception as e:
                ret = {"status": "faild", "message": "通过密码远程安装agent失败%s" % e}
                print(e)

        return JsonResponse(ret)

