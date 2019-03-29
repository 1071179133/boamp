from django.db.models import Q

def table_filter(request,admin_class):
    """进行条件过滤并返回过滤后的数据"""
    filter_conditions = {}
    keywords = ['page','o','_q','pg_num']
    for k,v in request.GET.items():     #request.GET.items：获取表单提交的数据
        if k in keywords: #分页保留的关键字和排序关键字，不能使用
            continue
        if v:
            filter_conditions[k] = v
    return admin_class.model.objects.filter(**filter_conditions).order_by('-id'),filter_conditions

def table_sort(request,admin_class,obj):
    """对数据进行排序"""
    orderby_key = request.GET.get("o")
    if orderby_key: #根据正负排序
        res = obj.order_by(orderby_key)
        if orderby_key.startswith("-"):
            orderby_key = orderby_key.strip("-")
        else:
            orderby_key = "-%s"%orderby_key
    else:
        res = obj
    return res,orderby_key

def table_search(request,admin_class,query_sets):
    """对数据模糊查询"""
    search_key = request.GET.get("_q","")
    q_obj = Q()
    q_obj.connector = "OR"
    for column in admin_class.search_fields:
        q_obj.children.append(("%s__contains"%column,search_key))   #字段名__contains 表示模糊查询
    res = query_sets.filter(q_obj)
    return res

