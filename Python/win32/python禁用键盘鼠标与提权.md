# 要求

利用python实现禁用键盘鼠标

# 思路

经过查阅资料目前最好的办法是采用ctypes中的dll文件进行编写

```python
from ctypes import *
improt time

print(winll.shell32.IsUserAnAdmin())  #判断是否有管理员权限


user32 = windll.LoadLibrary("C:\\Windows\\System32\\user32.dll")
user32.BlockInput(True)  #该功能需要管理员权限 True  禁用
time.sleep(5)
user32.BlockInput(Flase)  #该功能需要管理员权限 
time.sleep(5)         
```

# 提权

```python
def requireAdministrator(f):
    def inner(*args, **kwargs):
        if windll.shell32.IsUserAnAdmin():
            f()
        else:
            # Re-run the program with admin rights
            windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 0)
            f()
    return inner
```

[官方文档](https://docs.microsoft.com/zh-cn/windows/desktop/api/shellapi/nf-shellapi-shellexecutea)