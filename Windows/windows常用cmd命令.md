# cmd

## 列出所有端口占用

```
netstat -ano
```



## 根据端口名查找进程或者端口占用

```
netstat -ano|findstr "PROT OR PID"
```

## 根据PID查找进程名

```
tasklist|findstr "PID"
```

## 结束进程

```
taskkill /f /t /im "processName"
```

