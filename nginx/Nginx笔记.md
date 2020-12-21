# 1.Nginx知识网结构图

![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPxfoWRZoiamhfYPZKkGwS7ib3GJNeYA0NU00dJFkbibVoCdlCReRBSOPQg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
Nginx是一个高性能的HTTP和反向代理服务器，特点是占用内存少，并发能力强，事实上nginx的并发能力确实在同类型的网页服务器中表现较好

nginx专为性能优化而开发，性能是其最重要的要求，十分注重效率，有报告nginx能支持高达50000个并发连接数

## 1.1反向代理

**正向代理**
正向代理：局域网中的电脑用户想要直接访问网络是不可行的，只能通过代理服务器来访问，这种代理服务就被称为正向代理。
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPOicmLInzJxQaPU5Ria1rfK7G87tyH6PaXPfqsyn2DsjeemXddOkXPwpA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**反向代理**
反向代理：客户端无法感知代理，因为客户端访问网络不需要配置，只要把请求发送到反向代理服务器，由反向代理服务器去选择目标服务器获取数据，然后再返回到客户端，此时反向代理服务器和目标服务器对外就是一个服务器，暴露的是代理服务器地址，隐藏了真实服务器IP地址
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPk1VXGdVpwaJFp9BLxopwEYFyFibcRXXqeu6g7fRicESqx2PTwoxp1ibfQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

## 1.2负载均衡

客户端发送多个请求到服务器，服务器处理请求，有一些可能要与数据库进行狡猾，服务器处理完毕之后，再将结果返回给客户端

普通请求和响应过程
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPblbiaero6VACOibBJiadFxKh6h4rcBxnswZ52FKx0txDKpibQAdtIXeaxg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
但是随着信息数量增长，访问量和数据量飞速增长，普通架构无法满足现在的需求

我们首先想到的是升级服务器配置，可以由于摩尔定律的日益失效，单纯从硬件提升性能已经逐渐不可取了，怎么解决这种需求呢？

我们可以增加服务器的数量，构建集群，将请求分发到各个服务器上，将原来请求集中到单个服务器的情况改为请求分发到多个服务器，也就是我们说的负载均衡

**图解负载均衡**
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPXP7nvdt7A93y0fswYMVF6iaORlhmPrY3Iic5ydLVVic7b1GK0VZlc2AiaA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
假设有15个请求发送到代理服务器，那么由代理服务器根据服务器数量，平均分配，每个服务器处理5个请求，这个过程就叫做负载均衡

## 1.3动静分离

为了加快网站的解析速度，可以把动态页面和静态页面交给不同的服务器来解析，加快解析的速度，降低由单个服务器的压力

动静分离之前的状态
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPSq7o76cUicRCEgBgBA5F8vIemo8Zg7uNLopTBYpOzs7uCUlmZYhn10A/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
动静分离之后
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpP8ibibUEZaFtia7Q7xdZnTibLLz5icbakCAzcpgd6npNFicFO7dGSnA6ADxlA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

# 2. nginx如何在linux安装

https://blog.csdn.net/yujing1314/article/details/97267369

# 3. nginx常用命令

查看版本

```
./nginx -v
```

启动

```
./nginx
```

关闭（有两种方式，推荐使用 ./nginx -s quit）

```
 ./nginx -s stop
 ./nginx -s quit
```

重新加载nginx配置

```
./nginx -s reload
```

# 4.nginx的配置文件

配置文件分三部分组成

全局块
从配置文件开始到events块之间，主要是设置一些影响nginx服务器整体运行的配置指令

并发处理服务的配置，值越大，可以支持的并发处理量越多，但是会受到硬件、软件等设备的制约
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPyVnEH7vCTosam3IN1crgibialicgCrN8rPvQ4WgwfkAOfHJic7dWZtia6Rg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

events块
影响nginx服务器与用户的网络连接，常用的设置包括是否开启对多workprocess下的网络连接进行序列化，是否允许同时接收多个网络连接等等

支持的最大连接数
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPI7mC6O9F30DYyAYXjZcW7jYh5PUdY9aWTj3iaf6JGYtoPHJJlVU8zSA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
http块
诸如反向代理和负载均衡都在此配置

**location指令说明**

- 该语法用来匹配url，语法如下

```
location[ = | ~ | ~* | ^~] url{

}
```

1. =:用于不含正则表达式的url前，要求字符串与url严格匹配，匹配成功就停止向下搜索并处理请求
2. ~：用于表示url包含正则表达式，并且区分大小写。
3. ~*：用于表示url包含正则表达式，并且不区分大小写
4. ^~：用于不含正则表达式的url前，要求ngin服务器找到表示url和字符串匹配度最高的location后，立即使用此location处理请求，而不再匹配
5. 如果有url包含正则表达式，不需要有~开头标识

## 4.1 反向代理实战

**配置反向代理**
目的：在浏览器地址栏输入地址www.123.com跳转linux系统tomcat主页面

具体实现
先配置tomcat：因为比较简单，此处不再赘叙
并在windows访问
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPqm1pR3k5JQbjoSxCIbB9VF0oyibLSRSENqPMAickxRzB3eIsOZZg4E0Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
具体流程
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPYRUl1krfevicmpbxAMtZ5WjM7iaCJz34sibQ1shCKxLsJkWlSeT7GRnyA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
修改之前
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPAmfkznhOSicTlGziaAwKsCYGsejIKibTreO0kLda8nTrSnicMK0ydNKLPw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

配置
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPhia4YHqUhwHQlvJnb4IWX8iaJzQm0uVmXWP7MCJgqTQtzImgU42Zqa1Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
再次访问
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPhibaTwZ5tC2nIKibLficLiaJPSfCVqU0png9gcEk1ibFk9nKP7jHwYxM11w/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
**反向代理2**

1.目标
访问http://192.168.25.132:9001/edu/ 直接跳转到192.168.25.132:8080
访问http://192.168.25.132:9001/vod/ 直接跳转到192.168.25.132:8081

2.准备
配置两个tomcat，端口分别为8080和8081，都可以访问，端口修改配置文件即可。
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPrnezu8ua5OepazjE9ic42ajOiaDG7KFIEczdHXyaibI20icRZiaGODxNR7A/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPbx6t2rKbnFP0x7Vias0Qmram3aG5zCZmD5tjVALhHVUmFveWwPR8LPg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

新建文件内容分别添加8080！！！和8081！！！
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPN6oc70ELfQsoogTGk4KnBYVRQ7kg9b7MV79vuE9862uO3rfvLib0Lzw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPfIxMR6QCaGz8GxcqVytYakc5OOGksGIicWzrJxRnbSpV0KRzGVD2vHA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
响应如下
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPRvNAO4woxEAhZgoS4ezg8ibXqwxkgA2n7e6YsE9cVZktfvhS9MribPrg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPl6fwHvVkXibXAb3bcxTYXSFX0dFOD2CWnbruLoYN0KISGDKbGBlM3JA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
3.具体配置
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpP3IYPcAO2WFQ6ic2PHe6A7Dp3iaAG5IPL6TIcMFHibLhoV2GsIF6zW4vlg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
重新加载nginx

```
./nginx -s reload
```

访问
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPLVJP4vad88WchIVytXhyicKJBnI8wCPwlWiaA4YsZbWQ8lVKnXvCrO0w/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPLVJP4vad88WchIVytXhyicKJBnI8wCPwlWiaA4YsZbWQ8lVKnXvCrO0w/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
实现了同一个端口代理，通过edu和vod路径的切换显示不同的页面

## 4.2 反向代理小结

第一个例子：浏览器访问www.123.com，由host文件解析
出服务器ip地址

192.168.25.132 www.123.com
然后默认访问80端口，而通过nginx监听80端口代理到本地的8080端口上，从而实现了访问www.123.com，最终转发到tomcat 8080上去

第二个例子：
访问http://192.168.25.132:9001/edu/ 直接跳转到192.168.25.132:8080
访问http://192.168.25.132:9001/vod/ 直接跳转到192.168.25.132:8081

实际上就是通过nginx监听9001端口，然后通过正则表达式选择转发到8080还是8081的tomcat上去

## 4.3 负载均衡实战

1.修改nginx.conf
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPpFs52rxwjvncjYiceoBw2G7rOcLRiaq1bZPRDMlpJoUta8uJoBco6WYA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPWjhhcNWgQXKcl4BYcERgDeHAuP5JDzIF7UFt50pOMgtokwUuG7H29Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
2.重启nginx

```
./nginx -s reload
```

3.在8081的tomcat的webapps文件夹下新建edu文件夹和a.html文件，填写内容为8081！！！！

4.在地址栏回车，就会分发到不同的tomcat服务器上
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPbQVOGFv696oC4JA30y0FOdTo8GfJVfAboCTDEV78oDicZlFYqb61akA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPOBKSjzy767tnpExHIgH6CAIEGxdCkLxrzP6pxbPrbK5ib7vYa3FzqnQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
3.负载均衡方式

- 轮询（默认）
- weight，代表权，权越高优先级越高
    ![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPV30HKYCNbS4SEicdQgeMibEiautb45J5sMC0YJR2uFYyl0FpjaFlwtdEg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
- fair，按后端服务器的响应时间来分配请求，相应时间短的优先分配
    ![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPuzA0jWoNBsADUKLS5iaia1qWicMP87gIvZQsd9xcEOuMmhelnXYiaBo6Ng/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
- ip_hash,每个请求按照访问ip的hash结果分配，这样每一个访客固定的访问一个后端服务器，可以解决session 的问题
    ![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpP3LpwqjK4mpcDWQLiasaJEjwNRmRF1p8iabIrA1MIrG7wibUydW3iaZI6QA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

## 4.4 动静分离实战

**什么是动静分离**
把动态请求和静态请求分开，不是讲动态页面和静态页面物理分离，可以理解为nginx处理静态页面，tomcat处理动态页面

动静分离大致分为两种：一、纯粹将静态文件独立成单独域名放在独立的服务器上，也是目前主流方案；二、将动态跟静态文件混合在一起发布，通过nginx分开

**动静分离图析**
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPIPnBhLTpk5HLZicK3WKtUj4asw55uBALf8CIScKyvXU11Nua5EUJ7CA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
**实战准备**
准备静态文件

![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPiatxZm5ianAQlKibC7psUPtn4YicYEkSdtOOlOJtr7dKD59a4z1cXu2DCg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPKphmIcvibax41ia1PJxW8q2IbicDicsESIpvn1kOM6aM2kHXBLMjYMicHLw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
配置nginx
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPVtXnc0wnGGAvjl2tMTOm5NKXOI8icQK7mOgbBhIkwsbIboCHd3NcmWA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

# 5.nginx高可用

如果nginx出现问题
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPpiaZ6W4wvMW5Qevs0Xf1u2vWA3xK95r0rODqLj97jcCAXwEUZQdicLDQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
解决办法
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPW3gkZwZNUQIYyZ0LwlZqEwhLzgdu8Boh95hPtDBA0Scr3FibTZSjKFw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
前期准备

1. 两台nginx服务器
2. 安装keepalived
3. 虚拟ip

## 5.1安装keepalived

```
[root@192 usr]# yum install keepalived -y
[root@192 usr]# rpm -q -a keepalived
keepalived-1.3.5-16.el7.x86_64
```

修改配置文件

```
[root@192 keepalived]# cd /etc/keepalived
[root@192 keepalived]# vi keepalived.conf 
```

分别将如下配置文件复制粘贴，覆盖掉keepalived.conf
虚拟ip为192.168.25.50

> 对应主机ip需要修改的是
> smtp_server 192.168.25.147（主）smtp_server 192.168.25.147（备）
> state MASTER（主） state BACKUP（备）

```
global_defs {
   notification_email {
     acassen@firewall.loc
     failover@firewall.loc
     sysadmin@firewall.loc
   }
   notification_email_from Alexandre.Cassen@firewall.loc
   smtp_server 192.168.25.147
   smtp_connect_timeout 30
   router_id LVS_DEVEL # 访问的主机地址
}

vrrp_script chk_nginx {
  script "/usr/local/src/nginx_check.sh"  # 检测文件的地址
  interval 2   # 检测脚本执行的间隔
  weight 2   # 权重
}

vrrp_instance VI_1 {
    state BACKUP    # 主机MASTER、备机BACKUP    
    interface ens33   # 网卡
    virtual_router_id 51 # 同一组需一致
    priority 90  # 访问优先级，主机值较大，备机较小
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.25.50  # 虚拟ip
    }
}
```

启动

```
[root@192 sbin]# systemctl start keepalived.service
```

![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPaRNMNT2DjP7dZS1DZ3lJAt65JBGtSBMC6zsBaic1HMASs4A0y44oYzg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
访问虚拟ip成功
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPoIVx0XDN20OHbicp90H22BHIUbkLddqQL3ND7bnicDvO0uoILlFaLhlg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
关闭主机147的nginx和keepalived，发现仍然可以访问

# 6.原理解析

![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPZic5F4AaqoXIzdVMTIFwCtwrEovmqctZAC5l3iaOoiaGEElUFfkFYMGNw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
如下图，就是启动了一个master，一个worker，master是管理员，worker是具体工作的进程
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpPNFmGxKBxMhQjJj8KictJdqcx7pqQu8DFQyXQZzEicwIWYNzfAib7sibcqw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
worker如何工作
![图片](https://mmbiz.qpic.cn/mmbiz_png/1NOXMW586utV0VOSvEjM6ACsnNe71mpP4JpTGGVqTfcP88SiamK98G6z3YKaxm6mPILicJB5Y9bJoJoRHZmmqrpg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

# 小结

- worker数应该和CPU数相等
- 一个master多个worker可以使用热部署，同时worker是独立的，一个挂了不会影响其他的