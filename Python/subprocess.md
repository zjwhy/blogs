# cmd 结束进程树

## 背景

windows系统下，在程序中调用外部程序，类似于多进程概念，再杀掉程序后，启动的外部程序依旧运行。



## 调用程序

```
 print(os.getpid())
    ret = subprocess.Popen(r'D:\Desktop\GJJJ\datahandle0.2\dist\timeInput.exe', shell=True, stdout=subprocess.PIPE,)
    returncode = ret.poll()

    print(returncode)
    remp_cmd = ''
    while returncode is None:  # returncode None正在运行 0 正常结束 1 sleep 2 子程序不存在
        retline = ret.stdout.readline().strip()
        print(retline)
        if retline:
            remp_cmd = retline
        returncode = ret.poll()
        if remp_cmd == b"rpa_success" or remp_cmd == b"rpa_fail":
            break
        print(returncode)
    ret.kill()
  
 “”“
 该部分程序实现阻塞式调用外部程序，并且将外部程序shell输出到到主程序中
 ”“”
```

# 解决方案

shellexclude使用 cmd 命令结束进程树

```
taskkill /f /t /im python.exe
```

