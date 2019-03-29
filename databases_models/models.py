from django.db import models
# Create your models here.

class Project(models.Model):
    """项目表"""
    name = models.CharField(max_length=128,blank=False,null=False,verbose_name="项目名称")
    describe = models.CharField(max_length=512,blank=True,null=True,verbose_name="项目描述")
    create_time= models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "项目表"
        db_table = "project"

class UserType(models.Model):
    """用户类型表"""
    name = models.CharField(max_length=64,blank=False,null=False,verbose_name="用户类型")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "用户类型表"
        db_table = "usertype"

class User(models.Model):
    """用户表"""
    name = models.CharField(max_length=64,blank=False,null=False,verbose_name="用户名")
    password = models.CharField(max_length=64,blank=False,null=False,verbose_name="密码")
    usertype = models.ForeignKey("UserType",on_delete=models.CASCADE,verbose_name="用户类型")
    phone = models.CharField(max_length=64,blank=True,null=True,verbose_name="联系号码")
    phone_bak = models.CharField(max_length=64, blank=True, null=True, verbose_name="备用联系号码")
    project = models.ManyToManyField("Project",verbose_name="用户负责的项目")
    motto = models.CharField(max_length=512,blank=True,null=True,verbose_name="座右铭")
    hobby = models.CharField(max_length=512,blank=True,null=True,verbose_name="兴趣爱好")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "用户表"
        db_table = "user"

class ServerHost(models.Model):
    """机器表"""
    host_name = models.CharField(max_length=64,blank=True,null=True,verbose_name="名字")
    host_ip = models.CharField(max_length=64,blank=True,null=True,verbose_name="ip地址")
    host_port = models.IntegerField(verbose_name="ssh端口")
    b_project = models.ForeignKey("Project",on_delete=models.CASCADE,verbose_name="属于哪个项目")
    #user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="属于哪个用户")
    user = models.ManyToManyField("User",verbose_name="属于哪个用户")     #就不应该让它存在，让项目来控制就好
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.host_ip

    class Meta:
        verbose_name_plural = "机器表"
        db_table = "serverhost"

class MyAuthType(models.Model):
    """认证类型"""
    auth_type = models.CharField(max_length=32,blank=False,null=False,verbose_name="认证类型")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.auth_type

    class Meta:
        verbose_name_plural = "认证类型"
        db_table = "myauthtype"

class SecretKey(models.Model):
    """密钥表"""
    user = models.ForeignKey("User",on_delete=models.CASCADE,verbose_name="属于哪个用户")
    login_user = models.CharField(max_length=32,blank=True,null=True,verbose_name="登陆用户")
    auth_type = models.ForeignKey("MyAuthType",on_delete=models.CASCADE,verbose_name="认证类型")
    key = models.TextField(blank=True,null=True,verbose_name="密钥字符串")
    key_password = models.CharField(max_length=128,blank=True,null=True,verbose_name="密钥解密密码/用户密码")     #为了安全，启用密码自动认证
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.login_user

    class Meta:
        verbose_name_plural = "密码表"
        db_table = "secretkey"

class TaskList(models.Model):
    """任务表"""
    name = models.CharField(max_length=128,blank=True,null=True,verbose_name="任务名称")
    op_task = models.CharField(max_length=512,blank=True,null=True,verbose_name="执行内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    status_choices = (
        (0, "未执行"),
        (1, "已执行"),
        (2, "执行中"),
        (3, "不执行"),
    )
    status = models.SmallIntegerField(choices=status_choices,default=3,verbose_name="执行状态")
    done_time = models.DateTimeField(auto_now=True, verbose_name="完成时间")
    user = models.OneToOneField("User",on_delete=models.CASCADE,verbose_name="属于哪个用户")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "任务表"
        db_table = "tasklist"

class TaskRes(models.Model):
    """执行结果表"""
    res_content = models.TextField(verbose_name="执行结果")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    task = models.OneToOneField("TaskList",on_delete=models.CASCADE,verbose_name="属于哪个任务")

    def __str__(self):
        return self.task

    class Meta:
        verbose_name_plural = "执行结果表"
        db_table = "taskres"

class AuditLog(models.Model):
    """审计日志表"""
    op_content = models.CharField(max_length=512,blank=True,null=True,verbose_name="审计内容")
    op_host = models.OneToOneField("ServerHost",on_delete=models.CASCADE,verbose_name="操作关联机器")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.op_host

    class Meta:
        verbose_name_plural = "审计日志表"
        db_table = "auditlog"

class DevRecord(models.Model):
    """开发记录表"""
    content = models.CharField(max_length=512,blank=True,null=True,verbose_name="开发内容")
    name = models.CharField(max_length=32,blank=True,null=True,verbose_name="开发人")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="开发时间")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = "开发记录表"
        db_table = "devrecord"