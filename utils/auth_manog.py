from django.shortcuts import redirect

## 认证装饰器
def auth_manog_done(func):
    def inner(request,*args,**kwargs):
        if  not request.session.get("is_login", None):
            return redirect("/super_cmdb/login/")
        return func(request,*args,**kwargs)
    return inner