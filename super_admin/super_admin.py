from databases_models import models

enabled_admins = {}
#enabled_admins = {"app_name":"table_name"}

class BaseAdmin(object):
    list_display = []
    list_filters = []       #适用字段类型：choices ForeignKey DateTimeField DateField
    search_fields = []      #外键关联字段需要用'字段名__name'，关联的是id,要获取它的值才能查询
    filter_horizontal = ['tags','user','project']   #多对多字段名，加上则显示类django admin 复选框，否则是普通复选框
    list_per_page = 0       #每页显示条数[暂时没用了，使用session获取用户设定配置了]

# class CustomerAdmin(BaseAdmin):
#     #list_display = ['id','qq','name','source','consultant','date','status']
#     list_display = [    # 使用列表方式可以有序的显示中文字段
#         ["id","id"],
#         ["name", "姓名"],
#         ["qq", "qq号码"],
#         ["source", "来源"],
#         ["consultant", "销售顾问"],
#         ["status", "报名状态"],
#         ["date", "咨询时间"]
#     ]
#     #model = models.Customer
#     #list_filters = ['source','consultant','status','date']
#     list_filters = [    #使用列表方式可以有序显示中文过滤字段
#         ["source","来源"],
#         ["consultant", "销售顾问"],
#         ["status", "报名状态"],
#         ["date", "咨询时间"]
#     ]
#     search_fields = ['id','qq','name','consultant__name']
#
# class CustomerFollowUpAdmin(BaseAdmin):
#     #list_display = ['id','customer','content','consultant','intention','date']
#     list_display = [  # 使用列表方式可以有序的显示中文字段
#         ["id", "id"],
#         ["customer", "客户"],
#         ["content", "跟进内容"],
#         ["consultant", "跟进人"],
#         ["intention", "客户状态"],
#         ["date", "跟进时间"]
#     ]
#     #list_filters = ['customer','consultant','intention']
#     list_filters = [
#         ["consultant","跟进人"],
#         ["intention","客户状态"],
#         ["date", "时间"]
#     ]
#     search_fields = ['id','customer__name']

def register(models_class,admin_class=None):
    app_name = models_class._meta.app_label     #models_class._meta.app_label 获取app名字
    table_name = models_class._meta.model_name  #models_class._meta.model_name 获取table名字
    if app_name not in enabled_admins:
        enabled_admins[app_name] = {}
    admin_class.model = models_class    #绑定model对象和admin类  相当于24行的意思 赋admin_class 类下的model 值等于models_class表数据对象
    enabled_admins[app_name][table_name] = admin_class

class ProjectAdmin(BaseAdmin):
    #list_display = ['id','qq','name','source','consultant','date','status']
    list_display = [    # 使用列表方式可以有序的显示中文字段
        ["id","id"],
        ["name", "项目名"],
        ["create_time", "创建时间"],
        ["update_time", "更新时间"]
    ]
    #model = models.Customer
    #list_filters = ['source','consultant','status','date']
    list_filters = [    #使用列表方式可以有序显示中文过滤字段
        ["create_time", "创建时间"],
        ["update_time", "更新时间"]
    ]
    search_fields = ['id','name']

class ServerHostAdmin(BaseAdmin):
    #list_display = ['id','qq','name','source','consultant','date','status']
    list_display = [    # 使用列表方式可以有序的显示中文字段
        ["id","id"],
        ["host_name", "机器名"],
        ["host_ip", "ip"],
        ["host_port", "端口"],
        ["b_project", "隶属项目"],
        ["user", "隶属用户"],
        ["create_time", "创建时间"]
    ]
    #model = models.Customer
    #list_filters = ['source','consultant','status','date']
    list_filters = [    #使用列表方式可以有序显示中文过滤字段
        ["b_project", "隶属项目"],
        ["user", "隶属用户"],
        ["create_time", "创建时间"]
    ]
    search_fields = ['id','host_name','host_ip']

class UserAdmin(BaseAdmin):
    # list_display = ['id','qq','name','source','consultant','date','status']
    list_display = [  # 使用列表方式可以有序的显示中文字段
        ["id", "id"],
        ["name", "姓名"],
        ["usertype", "用户类型"],
        ["phone", "手机"],
        ["motto", "座右铭"],
        ["create_time", "创建时间"]
    ]
    # model = models.Customer
    # list_filters = ['source','consultant','status','date']
    list_filters = [  # 使用列表方式可以有序显示中文过滤字段
        ["usertype", "用户类型"],
        ["create_time", "创建时间"]
    ]
    search_fields = ['id', 'name', 'phone']


# register(models.Customer,CustomerAdmin)
# register(models.CustomerFollowUp,CustomerFollowUpAdmin)

register(models.Project,ProjectAdmin)
register(models.ServerHost,ServerHostAdmin)
register(models.User,UserAdmin)