#!/user/bin/python
#-*- coding:utf-8 -*-
#python版本需要2.7以上，否则不支持requests库

import hashlib,time
import requests,json
import psutil

ip = requests.get("http://members.3322.org/dyndns/getip").text.strip()
#定义token账号密码
name = 'xxxx'
password = 'xxxx'
#定义token 加盐
salt = 'xxx'


def encryption(token_str):
    md5 = hashlib.md5()  # 哈希加密
    md5.update(token_str.encode("utf-8"))  # utf8转换
    token = md5.hexdigest()  # 转成十六进制
    return token

while True:
    try:
        time_min = time.strftime('%Y-%m-%d_%H:%M')  #一分钟后token改变
        token_str = salt + name + password + time_min
        token = encryption(token_str)

        cpu_pyc_number = psutil.cpu_count(logical=False)        #物理cpu个数
        cpu_number = psutil.cpu_count()                         #cpu核数
        cpu_percent = psutil.cpu_percent()                      #cpu使用率
        cpu_time = psutil.cpu_times()                           #CPU的用户、系统、空闲时间
        memory = psutil.virtual_memory()                        #获取内存统计数据，单位bytes，我这里8G内存
        disk = psutil.disk_partitions()                         #获取磁盘分区信息
        #disk_usage = psutil.disk_usage('/')                                  #获取分区使用情况，这里使用了25.4%
        disk_io = psutil.disk_io_counters()                               #磁盘IO情况

        server_data = {
            "token":token,
            "ip":ip,
            "cpu":{
                "cpu_pyc_number": cpu_pyc_number,
                "cpu_number": cpu_number,
                "cpu_percent": cpu_percent,
                "cpu_time":{
                "cpu_user_time":cpu_time.user,
                "cpu_system_time":cpu_time.system,
                "cpu_iowait_time":cpu_time.iowait,
                "cpu_idle_time":cpu_time.idle,
                "cpu_nice_time":cpu_time.nice,
                "cpu_softirq_time":cpu_time.softirq,
                "cpu_irq_time":cpu_time.irq
                }
            },
            "memory":{
                "memory_total":memory.total/1024/1024,
                "memory_percent":memory.percent,
                "memory_available":memory.available/1024/1024,
                "memory_used":memory.used/1024/1024,
                "memory_free":memory.free/1024/1024,
            },
            "disk":{
                "disk_io":disk_io
            },
            "network":{}
        }

        url = 'http://139.159.157.135:4200/super_monitor/monitor_api/'
        headers = {'Content-Type': 'application/json'}    ## headers中添加上content-type这个参数，指定为json格式
        post_data = json.dumps(server_data)
        ret = requests.post(url,headers=headers, data=post_data)
        #print(ret,ret.text)
    except Exception as e:
        #print("出现异常：%s"%e)
        continue
    time.sleep(60)


