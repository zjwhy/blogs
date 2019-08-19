# 下载mysql-win 压缩包

[mysql-win安装包](https://dev.mysql.com/downloads/mysql/)

解压安装包，并放置合适位置

# 配置环境变量

添加PATH 环境变量   **D:\msyql-5.7.19-winx64\bin**

# 创建启动配置文件

my.ini

```
[mysqld]
#设置服务器字符集为utf8
character_set_server=utf8
collation-server=utf8_general_ci
#设置mysql的安装目录
basedir = D:\mysql-server
#设置mysql的数据文件存放目录
datadir = D:\mysql-server\data
#设置mysql服务所绑定的端口
port = 3306
#设置mysql允许的最大连接数
max_connections=15

[client]    
#设置客户端字符集
default-character-set=utf8
```

相关路径根据实际环境配置

# 安装mysql

管理员打开cmd，执行以下命令

首先初始化数据库

```
mysqld --initialize-insecure --usermysql
```

管理员启动cmd终端执行命令

```
mysqld -install
```

启动服务

```
net start mysql
```

# 登录mysql

```
mysql -u root -p
#直接回车，先不输入密码
```

# 设置root用户密码

```
 set password for root@localhost = password('123456');
```

# 设置远程访问权限

```
grant all privileges on *.* to root@'%' identified by '123456';
```

# 如果远程访问失败，请检查防火墙

windows 可以先把防火墙关了，如果关闭防火墙可以成功访问的话，可以添加一个入规则

协议TCP  端口3306 ，这样再打开防火墙就不会影响了。

liunx系列检查一下端口是否开放。

