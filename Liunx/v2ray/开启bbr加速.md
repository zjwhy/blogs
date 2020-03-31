#  CentOS 6 升级到指定内核 并启动BBR加速

先查看现在的内核

```
uname -r
```

以升级到4.18.20内核为例
kernel-ml-4.18.20-1.el6.elrepo.x86_64.rpm
kernel-ml-devel-4.18.20-1.el6.elrepo.x86_64.rpm
kernel-ml-headers-4.18.20-1.el6.elrepo.x86_64.rpm

下载内核

```
wget http://mirror.rc.usf.edu/compute_lock/elrepo/kernel/el6/x86_64/RPMS/kernel-ml-4.18.20-1.el6.elrepo.x86_64.rpm
wget http://mirror.rc.usf.edu/compute_lock/elrepo/kernel/el6/x86_64/RPMS/kernel-ml-devel-4.18.20-1.el6.elrepo.x86_64.rpm
wget http://mirror.rc.usf.edu/compute_lock/elrepo/kernel/el6/x86_64/RPMS/kernel-ml-headers-4.18.20-1.el6.elrepo.x86_64.rpm
```

安装内核

```
yum install kernel-ml-4.18.20-1.el6.elrepo.x86_64.rpm -y
yum install kernel-ml-devel-4.18.20-1.el6.elrepo.x86_64.rpm -y
yum install kernel-ml-headers-4.18.20-1.el6.elrepo.x86_64.rpm -y
```

查看已安装的内核

```
cat /boot/grub/grub.conf | awk '$1=="title" {print i++ " : " $NF}'
```

现有内核

0 : (4.18.20-1.el6.elrepo.x86_64)
1 : (2.6.32-754.11.1.el6.x86_64)
2 : (2.6.32-754.2.1.el6.x86_64)

发现第一位, 也就是0为刚刚安装的4.18.20

```
vi /boot/grub/grub.conf
```

修改配置文件

> default=0

重启电脑

```
reboot
```

查看现在的内核版本

```
uname -r
```

现在已经是

> 4.18.20-1.el6.elrepo.x86_64

开启BBR加速

```
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
```

然后使其生效

```
sysctl -p
```

查看BBR是否安装成功

```
sysctl net.core.default_qdisc
```

如果返回下面的信息

> net.core.default_qdisc = fq

再输入

```
sysctl net.ipv4.tcp_congestion_control
```

返回

> net.ipv4.tcp_congestion_control = bbr

或者

```
lsmod | grep tcp_bbr
```