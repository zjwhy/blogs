# 连接成功host警告

```
Warning: Permanently added the RSA host key for IP address '13.229.188.59' to the list of known hosts.
```

## 解决办法

liunx

```
vim /etc/hosts
添加 13.229.188.59 github.com
```

windows

```
C:\Windows\System32\drivers\etc\hosts  
添加 13.229.188.59 github.com
```

测试：

```
ssh -T git@github.com
```

