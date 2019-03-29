from django.db import models

# Create your models here.

class MonitorInfo(models.Model):
    """监控信息表"""
    ip = models.CharField(max_length=64,blank=True,null=True,verbose_name="ip地址")
    cpu_percent = models.CharField(max_length=64,blank=True,null=True,verbose_name="cpu使用率")
    cpu_user_time = models.CharField(max_length=64,blank=True,null=True,verbose_name="cpu用户时间")
    cpu_system_time = models.CharField(max_length=64,blank=True,null=True,verbose_name="cpu系统时间")
    cpu_iowait_time = models.CharField(max_length=64,blank=True,null=True,verbose_name="iowait_time")

    memory_total = models.CharField(max_length=64,blank=True,null=True,verbose_name="总内存")
    memory_percent = models.CharField(max_length=64,blank=True,null=True,verbose_name="内存使用率")
    memory_available = models.CharField(max_length=64,blank=True,null=True,verbose_name="可用内存")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")


    def __str__(self):
        return self.ip

    class Meta:
        verbose_name_plural = "监控信息表"
        db_table = "monitor_info"