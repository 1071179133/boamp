import paramiko
from threading import Thread
from webssh.tools.tools import get_key_obj
import socket
import json
from boamp.settings import logger

class SSH:
    def __init__(self, websocker, message):
        self.websocker = websocker
        self.message = message

    def connect(self, host, user, password, pkey=None, port=22, timeout=30,term='xterm', pty_width=80, pty_height=24):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if pkey:
                key = get_key_obj(paramiko.RSAKey, pkey_obj=pkey, password=password) or \
                      get_key_obj(paramiko.DSSKey, pkey_obj=pkey, password=password) or \
                      get_key_obj(paramiko.ECDSAKey, pkey_obj=pkey, password=password) or \
                      get_key_obj(paramiko.Ed25519Key, pkey_obj=pkey, password=password)

                print("使用密钥登陆")
                try:
                    ssh_client.connect(username=user, hostname=host, port=port, pkey=key, timeout=timeout)
                    logger.info("以[%s]用户通过[密钥]方式登陆机器[%s]成功"%(user,host))
                except Exception as e:
                    print("error：",e)
                    logger.warning("以[%s]用户通过[密钥]方式登陆机器[%s]失败，错误：%s" % (user, host,e))
            else:
                print("使用密码登陆")
                try:
                    ssh_client.connect(username=user, password=password, hostname=host, port=port, timeout=timeout)
                    logger.info("以[%s]用户通过[密码]方式登陆机器[%s]成功" % (user, host))
                except Exception as e:
                    print("error：",e)
                    logger.warning("以[%s]用户通过[密码]方式登陆机器[%s]失败，错误：%s" % (user, host, e))

            transport = ssh_client.get_transport()
            self.channel = transport.open_session()
            self.channel.get_pty(term=term, width=pty_width, height=pty_height)
            self.channel.invoke_shell()

            for i in range(2):
                recv = self.channel.recv(102400).decode('utf-8')
                self.message['status'] = 0
                self.message['message'] = recv
                message = json.dumps(self.message)
                self.websocker.send(message)

        except socket.timeout as e:
            self.message['status'] = 1
            self.message['message'] = 'ssh 连接超时'
            message = json.dumps(self.message)
            self.websocker.send(message)
            self.websocker.close()
        except Exception as e:
            self.message['status'] = 1
            self.message['message'] = str(e)
            message = json.dumps(self.message)
            self.websocker.send(message)
            self.websocker.close()

    def resize_pty(self, cols, rows):
        self.channel.resize_pty(width=cols, height=rows)


    def django_to_ssh(self, data):
        try:
            self.channel.send(data)
            return
        except:
            self.close()

    def websocket_to_django(self):
        try:
            while True:
                data = self.channel.recv(102400).decode('utf-8')
                if not len(data):
                    return
                self.message['status'] = 0
                self.message['message'] = data
                message = json.dumps(self.message)
                self.websocker.send(message)
        except:
            self.close()

    def close(self):
        self.message['status'] = 1
        self.message['message'] = '关闭连接'
        message = json.dumps(self.message)
        self.websocker.send(message)
        self.channel.close()
        self.websocker.close()

    def shell(self, data):
        Thread(target=self.django_to_ssh, args=(data,)).start()
        Thread(target=self.websocket_to_django).start()
