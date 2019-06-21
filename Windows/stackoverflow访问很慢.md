# stackoverflow访问很慢

1、更改host文件  文件地址： C:\Windows\System32\Drivers\etc 

​	如果不能直接修改，可拷贝到桌面修改后再复制回去

2、在host文件追加

```
127.0.0.1    ajax.googleapis.com
```

3、打开cmd执行dns刷新命令

​	

```cmd
ipconfig /flushdns
```

​	