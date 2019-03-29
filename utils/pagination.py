"""分页"""
class Page(object):
    def __init__(self,current_page,data_count,per_page_count=10,page_num=7):
        """
        初始化变量
        :param current_page: 当前页码，第几页
        :param data_count: 数据总条数
        :param per_page_count: 每页显示多少条数据，默认10条
        :param page_num: 显示多少个页码，默认7个
        """
        self.current_page = current_page
        self.data_count = data_count
        self.per_page_count = per_page_count
        self.page_num = page_num

    @property
    def start_count(self):
        return (self.current_page - 1) * self.per_page_count    #开始显示数据的起始数
    @property
    def end_count(self):
        return self.current_page * self.per_page_count  #结束显示数据条数

    @property
    def all_count_page(self):
        #数据总条数 除以 每页显示条数 等于 总页数
        all_page_num, remainder = divmod(self.data_count, self.per_page_count)  # divmod(101,10) 得到商和余数remainder,all_page_num为共有多少页
        if remainder:
            all_page_num += 1  # 如果有余数，则共有all_page_num+1 页
        return all_page_num

    def page_str(self,base_url):
        page_list = []  # 生成页码列表
        if self.all_count_page < self.page_num:   #我要取11个页码
            start_page = 1
            end_page = self.all_count_page + 1
        else:
            if self.current_page <= (self.page_num+1)/2:
                start_page = 1
                end_page = self.page_num + 1
            else:
                start_page = self.current_page - (self.page_num-1)/2
                end_page = self.current_page + (self.page_num+1)/2
                if (self.current_page + (self.page_num-1)/2) > self.all_count_page:
                    start_page = self.all_count_page - self.page_num + 1
                    end_page = self.all_count_page + 1
        ##上一页
        if self.current_page > 1:
            page_up = "<a class='prev' href='%s?Page=%s'>&lt;&lt;</a>" %(base_url,self.current_page-1)
            page_list.append(page_up)
        for page in range(int(start_page),int(end_page)):
            if page == self.current_page:
                page_str = "<a class='num' style='background: #009688; color: white' href='%s?Page=%s'>%s</a>" %(base_url,page,page)
            else:
                page_str = "<a class='num' href='%s?Page=%s'>%s</a>" % (base_url,page, page)
            page_list.append(page_str)
        ##下一页
        if self.current_page < self.all_count_page:
            page_down = "<a class='next' href='%s?Page=%s'>&gt;&gt;</a>" % (base_url,self.current_page + 1)
            page_list.append(page_down)
        ##尾页
        # if self.current_page + int(self.page_num/2) < self.all_count_page + int(self.page_num/2):
        #     page_last = "<a class='num' href='%s?Page=%s'>尾页</a>" %(base_url,self.all_count_page)
        #     page_list.append(page_last)
        #跳转页：
        jump_page = '''
            <select id="pg" onchange="changePageSize(this)" style="width: 74px;height: 38px">
                    <option value="13">13</option>
                    <option value="30">30</option>
                    <option value="50">50</option>
                    <option value="100">100</option>
                    <option value="1000">300</option>
            </select>条
        '''
        page_list.append(jump_page)
        ############################################分页逻辑结束############################################
        return page_list