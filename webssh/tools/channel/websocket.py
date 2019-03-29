from channels.generic.websocket import WebsocketConsumer
from webssh.tools.ssh import SSH
from django.http.request import QueryDict
from webssh import models
from django.utils.six import StringIO
import json
import base64


class WebSSH(WebsocketConsumer):
    message = {'status': 0, 'message': None}
    """
    status:
        0: ssh 连接正常, websocket 正常
        1: 发生未知错误, 关闭 ssh 和 websocket 连接

    message:
        status 为 1 时, message 为具体的错误信息
        status 为 0 时, message 为 ssh 返回的数据, 前端页面将获取 ssh 返回的数据并写入终端页面
    """

    def connect(self):
        try:
            self.accept()
            query_string = self.scope['query_string']
            connet_argv = QueryDict(query_string=query_string, encoding='utf-8')
            unique = connet_argv.get('unique')
            width = connet_argv.get('width')
            height = connet_argv.get('height')

            width = int(width)
            height = int(height)

            connect_info = models.HostTmp.objects.get(unique=unique)


            host = connect_info.host
            port = connect_info.port
            user = connect_info.user
            auth = connect_info.auth
            pwd = connect_info.password
            pkey = connect_info.pkey
            #print("web=============================pkey:",pkey)

            connect_info.delete()

            if pwd:
                password = base64.b64decode(pwd).decode('utf-8')        #这里解编码密码
            else:
                password = None

            self.ssh = SSH(websocker=self, message=self.message)

            if auth == 'key':
                pkey = pkey
                obj = StringIO()
                obj.write(pkey)
                obj.flush()
                obj.seek(0)
                self.pkey = obj
                #print("web=============================pkey:",self.pkey)

                self.ssh.connect(
                    host=host,
                    user=user,
                    password=password,
                    pkey=self.pkey,
                    port=port,
                    pty_width=width,
                    pty_height=height
                )
            else:
                self.ssh.connect(
                    host=host,
                    user=user,
                    password=password,
                    port=port,
                    pty_width=width,
                    pty_height=height
                )
        except Exception as e:      #因为上面解码时：base64.b64decode(pwd).decode('utf-8')，字符串原本没有编码，
                                     # 所以导致binascii.Error: Incorrect padding报错,所以后面添加密码时需要进行
                                     # 编码：base64.b64encode(b"root123456.")，修改后，密钥登陆的密码也需要编码
                                     # 原因是在webssh.js中编码了一下密钥登陆的password字段：var password = window.btoa(pwd); 已修改
                                     # 而使用密码登陆的没有经过此步骤，直接由后端查询数据库得到了
            print(e)
            self.message['status'] = 1
            self.message['message'] = str(e)
            message = json.dumps(self.message)
            self.send(message)
            self.close()

    def disconnect(self, close_code):
        try:
            self.ssh.close()
        except:
            pass

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if type(data) == dict:
            status = data['status']
            if status == 0:
                data = data['data']
                self.ssh.shell(data)
            else:
                cols = data['cols']
                rows = data['rows']
                self.ssh.resize_pty(cols=cols, rows=rows)
