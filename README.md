1.项目名称：boamp (Best Operational and Maintenance Platform) 命名方式有点...........

2.开发环境：Python 3.5.3 + Django==2.1.1 + X-admin + Bootstrap3.5

3.项目介绍：

    1.用户管理：实现用户的增删查改
    2.权限管理：超级管理员控制权限，用户可关联多个项目，项目下可拥有多台机器，机器只属于一个项目，但机器可属于多个用户，当新增用户并分配已有项目的权限时，会自动关联项目下的机器给该用户
    3.cmdb管理：包含密钥管理，机器列表，agent安装，域名解析，webssh等模块
    4.监控管理：通过安装监控agent，自动获取当前服务器状态及信息，并保存历史记录
    5.安全说明：(1)平台用户使用session认证，真实密码使用hashlib不可逆加密；(2)webssh使用密钥/密码认证，需要登陆平台的用户才能使用，由平台用户自行管理；(3)api接口使用动态token认证，生成token规则由超级管理员配置管理 平台使用说明
    1.使用流程：超级管理员创建用户 --> 超级管理员创建项目 --> 超级管理员分配项目权限给用户 --> 普通管理员添加管理自己的登陆方式(密钥/密码) --> 普通管理员对已有项目添加机器 --> 普通管理员对机器安装agent --> 实现对机器的日常维护管理
    2.超级管理员拥有最大管理权限，可管理用户、管理项目、分配用户对项目的权限，以及普通用户拥有的所有权限
    3.普通管理员受超级管理员限制，可对自己拥有项目的机器进行管理及配置

4.使用说明

    1.使用流程：超级管理员创建用户 --> 超级管理员创建项目 --> 超级管理员分配项目权限给用户 --> 普通管理员添加管理自己的登陆方式(密钥/密码) --> 普通管理员对已有项目添加机器 --> 普通管理员对机器安装agent --> 实现对机器的日常维护管理
    2.超级管理员拥有最大管理权限，可管理用户、管理项目、分配用户对项目的权限，以及普通用户拥有的所有权限
    3.普通管理员受超级管理员限制，可对自己拥有项目的机器进行管理及配置

5.安装配置

    1.配置settings.py 中的数据库信息(mysql)
    2.创建数据库：CREATE DATABASE IF NOT EXISTS boamp default charset utf8 COLLATE utf8_unicode_ci;
    3.配置api token 认证信息账号密码
    4.安装依赖标准库：pip install -r requirements.txt
    5.生成数据结构：python manage.py makemigrations && python manage.py migrate

6.运行：/usr/local/python35/bin/python3.5 manage.py runserver 0.0.0.0:8000 --insecure

7.访问地址：http://127.0.0.1:8000/super_cmdb/login/

8.初始账号密码
    root
    super_boamp
