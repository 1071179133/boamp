import os,paramiko

def get_key_obj(pkeyobj, pkey_file=None,password=None):
    if pkey_file:
        try:
            pkey = pkeyobj.from_private_key_file(filename=pkey_file, password=password)
            return pkey
        except Exception as e:
            print("from_private_key_file失败：",e)

def paramiko_ssh(ip=None,port=None,password=None,login_user=None,cmd=None,pkey_file=None):
    """远程执行命令函数"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if pkey_file:
        print("使用密钥登陆")
        pkey = get_key_obj(paramiko.RSAKey, pkey_file=pkey_file, password=password) or \
              get_key_obj(paramiko.DSSKey, pkey_file=pkey_file, password=password) or \
              get_key_obj(paramiko.ECDSAKey, pkey_file=pkey_file, password=password) or \
              get_key_obj(paramiko.Ed25519Key, pkey_file=pkey_file, password=password)
        try:
            ssh.connect(hostname=ip, port=port, username=login_user, pkey=pkey, timeout=20)
        except Exception as e:
            print("error：", e)
    else:
        print("使用密码登陆")
        try:
            ssh.connect(hostname=ip, port=port, username=login_user, password=password,timeout=20)
        except Exception as e:
            print("error：", e)


    stdin, stdout, stderr = ssh.exec_command(cmd)
    retcode = stdout.channel.recv_exit_status()
    result = stdout.read()
    ssh.close()
    return retcode,result

# aa = paramiko_ssh("115.xx.xxx.xx",22,"xxxxx","root","free -m","./Identity")
# aa = paramiko_ssh("139.xxx.xx.xx",22,"xxxxx.","root","free -m",pkey_file=None)
# print(aa)

def paramiko_scp(ip=None,port=None,password=None,login_user=None,source_filename=None,target_filename=None,pkey_file=None):
    if pkey_file:
        print("基于公钥密钥上传下载")
        pkey = get_key_obj(paramiko.RSAKey, pkey_file=pkey_file, password=password) or \
               get_key_obj(paramiko.DSSKey, pkey_file=pkey_file, password=password) or \
               get_key_obj(paramiko.ECDSAKey, pkey_file=pkey_file, password=password) or \
               get_key_obj(paramiko.Ed25519Key, pkey_file=pkey_file, password=password)
        transport = paramiko.Transport((ip, port))
        transport.connect(username=login_user, pkey=pkey)
        sftp = paramiko.SFTPClient.from_transport(transport)

    else:
        print("基于用户名密码上传下载")
        transport = paramiko.Transport((ip, port))
        transport.connect(username=login_user, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        # 将source_filename 上传至服务器 target_file_dir
        sftp.put(source_filename,target_filename)
        print("文件[%s]上传到服务器[%s]成功"%(source_filename,ip))
        # 将remove_path 下载到本地 local_path
        #sftp.get('remove_path', 'local_path')
        transport.close()
    except Exception as e:
        print("文件[%s]上传到服务器[%s]失败：%s" % (source_filename, ip,e))

#paramiko_scp("115.1xx",22,"xxxxx","root","./my_paramiko_ssh.py","/tmp/my_paramiko_ssh.py","./Identity")
#paramiko_scp("139.159xxx",22,"xxxxx.","root","./my_paramiko_ssh.py","/tmp/my_paramiko_ssh.py",pkey_file=None)
