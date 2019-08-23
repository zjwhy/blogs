#  系统环境

阿里云vps， hostwinds

ubuntu16

采用pptpd搭建vpn服务

# pptpd配置

1、 安装

```
sudo apt install pptpd
```

2、 修改pptpd.conf

```
vim /etc/pptpd.conf

取消一下两行注释， ip地址可以自行定义
# (Recommended)
#localip 192.168.0.1
#remoteip 192.168.0.234-238,192.168.0.245
```

3、 修改chap-secrets分配vpn账号

```
vim /etc/ppp/chap-secrets 
```

```shell
  1 # Secrets for authentication using CHAP
  2 # client    server  secret          IP addresses
  3 user  pptpd   passwd      *
```

​	*代表任何ip地址都可访问

4、 设置dns

```
vim /etc/ppp/pptpd-options 
```

```
#取消ms-dns注释
ms-dns 10.0.0.1
ms-dns 10.0.0.2


更改为谷歌dns
ms-dns 8.8.8.8
ms-dns 8.8.4.4

```

5、 开启内核IP转发

```
vim /etc/sysctl.conf 
```

```
取消该行注释
 net.ipv4.ip_forward=1
```

```
是更改即时生效
sysctl -p
```

6、配置iptables

```
安装
sudo apt install iptables
```

```
清除iptables以前的规则
sudo iptables -F
sudo iptables -X
sudo iptables -t nat -F
sudo iptables -t nat -X
```

```
允许gre协议以及1723端口、47端口
sudo iptables -A INPUT -p gre -j ACCEPT 
sudo iptables -A INPUT -p tcp --dport 1723 -j ACCEPT 
sudo iptables -A INPUT -p tcp --dport 47 -j ACCEPT
```

7、 开启NAT转发

```
我的网卡是ens3
sudo iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -o eth0 -j MASQUERADE
```

8、 重启pptpd服务

```
sudo service pptpd restart
```

