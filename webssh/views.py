from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from webssh.tools import tools
import json
from databases_models import models
from utils.auth_manog import auth_manog_done

#http://blog.51cto.com/hongchen99/2336087

@auth_manog_done
def index(request,port,host1,host2,host3,host4):
    if request.method == 'GET':
        user_id = request.session.get("user_id")
        # 默认是使用密钥登陆auth_type=1
        secret_key_info = models.SecretKey.objects.filter(user=user_id, auth_type=1).first()
        host = "%s.%s.%s.%s" % (host1, host2, host3, host4)
        return render(request, 'webssh/index.html',{"secret_key_info":secret_key_info,"host":host,"port":port})

@auth_manog_done
def ssh_connect(request):

    if request.method == 'POST':      #得到的是已编码过的密码
        user_id = request.session.get("user_id")
        # 默认是使用密钥登陆auth_type=1
        secret_key_info = models.SecretKey.objects.filter(user=user_id, auth_type=1).first()
        success = {'code': 0, 'message': None, 'error': None}

        try:
            post_data = request.POST.get('data')
            data = json.loads(post_data)
            #print(data)

            auth = data.get('auth')
            if auth == 'key':
                # pkey = request.FILES.get('pkey')
                # key_content = pkey.read().decode('utf-8')
                key_content = secret_key_info.key
                print("views:",key_content)
                data['pkey'] = key_content
            else:
                #当前端返回的登陆方式不是密钥，则使用密码登陆auth_type=2
                secret_key_info_new = models.SecretKey.objects.filter(user=user_id,auth_type=2).first()
                data['password'] = data.get('password')
                #data['password'] = secret_key_info_new.key_password
                data['user'] = secret_key_info_new.login_user

            unique = tools.unique()
            data['unique'] = unique

            #print(data)
            valid_data = tools.ValidationData(data)

            if valid_data.is_valid():
                valid_data.save()
                success['message'] = unique
            else:
                error_json = valid_data.errors.as_json()
                success['code'] = 1
                success['error'] = error_json

            return JsonResponse(success)
        except Exception as e:
            success['code'] = 1
            success['error'] = '密钥、密码不正确或未录入登陆方式，请校对'
            print(success)
            return JsonResponse(success)
