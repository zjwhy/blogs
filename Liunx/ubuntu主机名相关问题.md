# ubuntu主机名相关问题

1、修改hostname 文件

该文件中的内容是显示的主机名

```
sudo vim /etc/hostname
```

2、修改hosts 文件

如果执行sudo命令出现

```
sudo: unable to resolve host
（无法解析主机）
```

修改 hosts文件 将127.0.0.1 后的内容改为主机名

```
sudo vim /etc/hosts
```

内容：

```
127.0.0.1       localhost
				
# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

将localhost改为主机名



3、更改完后 重启主机

```
sudo reboot
```

