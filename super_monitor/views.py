from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from utils.hashlib_done import encryption
import hashlib,time,json
from django.views.decorators.csrf import csrf_exempt
from super_monitor import models
from databases_models import models as all_models
from utils.auth_manog import auth_manog_done

from boamp.settings import token_name,token_password,token_salt

def get_now_token():
    token_time_min = time.strftime('%Y-%m-%d_%H:%M')  # 一分钟后token改变
    token_str = token_salt + token_name + token_password + token_time_min
    token = encryption(token_str)
    return token
# Create your views here.

@csrf_exempt
def monitor_api(request):
    if request.method == "POST":
        current_token = get_now_token()
        data = json.loads(str(request.body, encoding="utf8"))   #request.body 是提交的数据为byte类型，转换成字符串类型再转换成字典
        #print(data,type(data))
        get_token = data["token"]
        if current_token == get_token:
            save_data = {
                "ip": data["ip"],
                "cpu_percent": data["cpu"]["cpu_percent"],
                "cpu_user_time": data["cpu"]["cpu_time"]["cpu_user_time"],
                "cpu_system_time": data["cpu"]["cpu_time"]["cpu_system_time"],
                "cpu_iowait_time": data["cpu"]["cpu_time"]["cpu_iowait_time"],
                "memory_total": data["memory"]["memory_total"],
                "memory_percent": data["memory"]["memory_percent"],
                "memory_available": data["memory"]["memory_available"],
            }
            try:
                if all_models.ServerHost.objects.filter(host_ip=save_data["ip"]).first():
                    models.MonitorInfo.objects.create(**save_data)
                    ret = {"Status Code:": 200, "status": "success", "message": "数据提交成功"}
                else:
                    ret = {"Status Code:": "null", "status": "faild", "message": "平台还没添加该机器ip，不允许记录数据"}
                return JsonResponse(ret)
            except Exception as e:
                message = "插入数据失败：" + e
                ret = {"Status Code:": "null", "status": "faild", "message": message}
                return JsonResponse(ret)
        else:
            ret = {"Status Code:": "null", "status": "faild", "message": "数据提交失败"}
            return JsonResponse(ret)

@auth_manog_done
def monitor_list(request):
    if request.method == "GET":
        monitor_lists = []
        host_list = all_models.ServerHost.objects.all()
        for host in host_list:
            host_ip = host.host_ip
            monitor_info = models.MonitorInfo.objects.filter(ip=host_ip).order_by("-create_time")[:1]
            if monitor_info:
                monitor_lists.append(monitor_info)
        return render(request,"super_monitor/monitor_list.html",{"monitor_lists":monitor_lists})

@auth_manog_done
def monitor_history(request):
    if request.method == "GET":
        monitor_lists = models.MonitorInfo.objects.all().order_by("-create_time")[:500]
        return render(request, "super_monitor/monitor_history.html", {"monitor_lists": monitor_lists})
    elif request.method == "POST":
        ip = request.POST.get("ip")
        monitor_lists = models.MonitorInfo.objects.filter(ip=ip).order_by("-create_time")
        return render(request, "super_monitor/monitor_history.html", {"monitor_lists": monitor_lists})