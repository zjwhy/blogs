1、更改host文件  文件地址： C:\Windows\System32\Drivers\etc 

​	如果不能直接修改，可拷贝到桌面修改后再复制回去

2、在host文件追加

​	

```c
#github
192.30.253.112 github.com 

151.101.113.194 github.global.ssl.fastly.net
```

​	ip 地址通过以下两个网站可查

​	<http://github.com.ipaddress.com/> 

​	<http://github.global.ssl.fastly.net.ipaddress.com/> 



3、打开cmd执行dns刷新命令

​	

```cmd
ipconfig /flushdns
```

​	

