
"""访问限制"""

# 1：超级管理员
# 2：管理员
# 配置:
    # 在对应的列表中加入请求url，并在需要限制权限的views函数中加入判断以下即可：
"""
    if access_rt(request,models) == permission_status:#判断是否有权限访问函数
        return HttpResponse(permission_status)
    else:
"""

def access_rt(request,models):
    access_list = {
        "1":[],
        "2":[
            "/super_cmdb/user_list/",
            "/super_cmdb/user_add/",
            "/super_cmdb/user_del/",
            "/super_cmdb/project_list/",
            "/super_cmdb/project_add/",
            "/super_cmdb/project_edit/",
            "/super_cmdb/project_del/",
            "/super_cmdb/permission_set/",
        ],
    }
    request_url = request.path
    user_id = request.session.get("user_id")
    usertype_id = models.User.objects.filter(id=user_id).first().usertype_id
    if request_url in access_list["%s"%usertype_id]:
        print("你没有此页面的访问权限，请退出")
        return "permission denied"