# 卸载Teamviwer

卸载Teamviwer，删除配置文件，

删除注册表

​	计算机\HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\TeamViewer

​	计算机\HKEY_CURRENT_USER\Software\TeamViewer





# 修改mac地址

1、控制面板\网络和 Internet\网络连接

2、找到mac当前网络连接 右击属性=》 配置 =》高级 =》修改 网络地址（有的叫物理地址，networaddress）

3、更改16进制mac地址，网络重新连接。部分机器需要重启

4、cmd 命令 ipconfig \all 检查mac地址是否更改



# 没有网络地址选项

这种情况是由于woindws进行了隐藏，可以通过以下办法 跳出配置

## 新建项

```
计算机\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}\0008\Ndi\Params\NetworkAddress
```

## 新建值

```
LimitText	12
optional	1
ParamDesc	网络地址
type	edit
UpperCase	1
```



注册表更改完后，再根据更改mac地址进行更改



如果修改失败，请下载软件修改

<https://technitium.com/tmac/>