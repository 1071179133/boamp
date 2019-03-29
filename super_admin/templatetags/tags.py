from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta    #时间运算用timedelta
register = template.Library()

@register.simple_tag
def render_table_name(admin_class):
    """获取表中文名并返回"""
    return admin_class.model._meta.verbose_name_plural

##在分页中需要后端处理逻辑，所以不能使用templatetags从前端直接取数据，被弃用
# @register.simple_tag
# def get_query_sets(admin_class):
#     return admin_class.model.objects.all()

@register.simple_tag
def build_table_row(request,obj,admin_class):
    """创建并返回表数据"""
    row_ele = ""
    for index,column in enumerate(admin_class.list_display):
        """
        models.CustomerInfo._meta.fields   获取model所有字段的对象
        models.CustomerInfo._meta.get_field('status')   取一个字段的对象
        get_xxxx_display       显示choices里面的值
        getattr() 函数用于返回一个对象属性值。
        """

        column = column[0]
        field_obj = obj._meta.get_field(column)
        if field_obj.choices:   #判断是否是choices类型
            column_data = getattr(obj,"get_%s_display" %column)()
        elif type(field_obj).__name__ == 'ManyToManyField':     #没找到处理方法
            column_data = field_obj
        else:
            column_data =  getattr(obj,column)
        if type(column_data).__name__ == 'datetime':    #判断字段是否是日期，做转换
            column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")

        if index == 0 or index == 1: #add href ,跳转到修改页链接
            column_data = "<a href='{request_path}{obj_id}/change/'>{data}</a>".format(request_path=request.path,obj_id=obj.id,data=column_data)

        row_ele += "<td>%s</td>"%column_data
    #print(row_ele)
    return mark_safe(row_ele)

@register.simple_tag
def render_page_ele(loop_counter,query_sets,filter_conditions,previous_orderby,search_text):
    """创建并返回页码"""
    filters = ''
    for k, v in filter_conditions.items():
        filters += "&%s=%s" % (k, v)
    if abs(query_sets.number - loop_counter) <= 6:  #6: 控制显示多少个页码
        ele_class = ""
        if query_sets.number == loop_counter:
            ele_class = "active"
        ele = """<li class="%s"><a href="?page=%s%s&o=%s&_q=%s">%s</a></li>"""%(ele_class,loop_counter,filters,previous_orderby,search_text,loop_counter) #返回的页码带有过滤条件及排序
        return mark_safe(ele)
    return ''

@register.simple_tag
def render_url(filter_conditions,previous_orderby,search_text):
    """创建并返回上下首尾页的url参数"""
    filters = ''
    for k, v in filter_conditions.items():
        filters += "&%s=%s" % (k, v)
    res = "%s&o=%s&_q=%s"%(filters,previous_orderby,search_text)
    return mark_safe(res)

@register.simple_tag
def render_filter_ele(condtion,admin_class,filter_conditions):
    """创建并返回检索下拉框数据"""
    #select_ele = '''<select class='form-control' name='%s'> <option value=''>---</option>'''%condtion
    select_ele = '''<select class='form-control' name='{filter_field}'> <option value=''>---</option>'''
    field_obj = admin_class.model._meta.get_field(condtion)
    selected = ''
    if field_obj.choices:
        for choice_item in field_obj.choices:
            if filter_conditions.get(condtion) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>'''%(choice_item[0],selected,choice_item[1])
            selected = ''
    if type(field_obj).__name__ == "ForeignKey":
        for choice_item in field_obj.get_choices()[1:]:
            if filter_conditions.get(condtion) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0],selected,choice_item[1])
            selected = ''
    if type(field_obj).__name__ in ['DateTimeField','DateField']:
        date_els = []
        today_ele = datetime.now().date()   #今天
        date_els.append(['今天', datetime.now().date()])
        date_els.append(['昨天', today_ele - timedelta(days=1)])
        date_els.append(['近7天', today_ele - timedelta(days=7)])
        date_els.append(['本月', today_ele.replace(day=1)])
        date_els.append(['近30天', today_ele - timedelta(days=30)])
        date_els.append(['近90天', today_ele - timedelta(days=90)])
        date_els.append(['近180天', today_ele - timedelta(days=180)])
        date_els.append(['今年', today_ele.replace(month=1,day=1)])
        date_els.append(['近1年', today_ele - timedelta(days=365)])

        for item in date_els:
            if filter_conditions.get("create_time__gte") == str(item[1]) :
                selected = 'selected'
            select_ele += '''<option value='%s' %s>%s</option>''' % (item[1],selected,item[0])
            selected = ''
        filter_field_name = "%s__gte"%condtion
    else:
        filter_field_name = condtion
    select_ele += "</select>"
    select_ele = select_ele.format(filter_field=filter_field_name)

    return mark_safe(select_ele)

@register.simple_tag
def build_table_header_column(column,column_zh_name,orderby_key,filter_conditions):
    filters = ''
    for k, v in filter_conditions.items():
        filters += "&%s=%s" % (k, v)

    ele = '''
    <th>
        <a href="?{filters}&o={orderby_key}">{column}</a>
        {sort_icon}
    </th>
    '''
    if orderby_key:
        if orderby_key.startswith("-"):
            sort_icon = '''<span class="glyphicon glyphicon-menu-up" aria-hidden="true" style="font-size: 1px"></span>'''
        else:
            sort_icon = '''<span class="glyphicon glyphicon-menu-down" aria-hidden="true" style="font-size: 1px"></span>'''

        if orderby_key.strip("-") == column:    #判断是否是排序的字段
            orderby_key = orderby_key
        else:
            orderby_key = column
            sort_icon = ''
    else:
        orderby_key = column
        sort_icon = ''
    ele = ele.format(filters=filters,orderby_key=orderby_key,column=column_zh_name,sort_icon=sort_icon)
    return mark_safe(ele)


@register.simple_tag
def get_m2m_obj_list(admin_class,field,form_obj):
    """返回m2m复选框所有待选数据"""
    field_obj = getattr(admin_class.model,field.name)     #表结构对象中的某个字段[动态]
    #models.Customer.tags.rel.model.objects.all()   #多对多中查询主表的所有数据
    all_obj_list = field_obj.rel.model.objects.all()    #某个字段[动态]的所有数据

    if form_obj.instance.id: #判断model form 是否存在数据
        obj_instance_field = getattr(form_obj.instance,field.name)   #单条数据对象中的某个字段
        selected_obj_list = obj_instance_field.all()    #已经选择的数据
    else:
        return all_obj_list

    standby_ibj_list = []
    for obj in all_obj_list:        #过滤掉已选的数据
        if obj not in selected_obj_list:
            standby_ibj_list.append(obj)

    return standby_ibj_list

@register.simple_tag
def get_m2m_selected_obj_list(form_obj,field):
    '''返回复选框已选中的m2m数据'''
    if form_obj.instance.id:
        field_obj = getattr(form_obj.instance,field.name)   #执行了此操作：a = models.Customer.objects.last() && getattr(a,'tags').all()
        return field_obj.all()

def recursive_related_objs_lookup(objs,mode_name):
    """递归查找关联关系"""
    mode_name = objs[0]._meta.model_name
    ul_ele = "<ul>"
    for obj in objs:
        li_ele = '''<li>%s:%s</li>'''%(obj._meta.verbose_name_plural,obj.__str__().strip("<>"))
        ul_ele += li_ele

        #for local many many
        for m2m_field in obj._meta.local_many_to_many:
            sub_ul_ele = "<ul>"
            m2m_field_obj = getattr(obj,m2m_field.name)
            for o in m2m_field_obj.select_related():
                li_ele = '''<li>%s:%s</li>''' % (m2m_field.verbose_name, o.__str__().strip("<>"))
                sub_ul_ele += li_ele
            sub_ul_ele += "</ul>"
            ul_ele +=sub_ul_ele

        for related_obj in obj._meta.related_objects:
            if 'ManyToOneRel' not in related_obj.__repr__():
                continue
            if 'ManyToManyRel' in related_obj.__repr__():
                if hasattr(obj,related_obj.get_accessor_name()):
                    accessor_obj = getattr(obj,related_obj.get_accessor_name())
                    if hasattr(accessor_obj,"select_related"):  #select_related == all
                        target_objs = accessor_obj.select_related()
                    sub_ul_ele = "<ul style='color:red'>"
                    for o in target_objs:
                        li_ele = '''<li>%s:%s</li>''' % (o._meta.verbose_name, o.__str__().strip("<>"))
                        sub_ul_ele += li_ele
                    sub_ul_ele += "</ul>"
                    ul_ele += sub_ul_ele

            elif hasattr(obj,related_obj.get_accessor_name()):
                accessor_obj = getattr(obj,related_obj.get_accessor_name())
                if hasattr(accessor_obj,"select_related"):  #select_related == all
                    target_objs = accessor_obj.select_related()
                else:
                    target_objs = accessor_obj
                if len(target_objs) > 0:
                    nodes = recursive_related_objs_lookup(target_objs,mode_name)
                    ul_ele += nodes
    ul_ele += "</ul>"
    return ul_ele


@register.simple_tag
def display_all_rekated_objs(obj):
    """把对象及所有关联的数据取出来"""
    objs = [obj,]
    if objs:
        model_class = objs[0]._meta.model
        mode_name = objs[0]._meta.model_name
        return mark_safe(recursive_related_objs_lookup(objs,mode_name))