# 打包进程相关代码失败

例如编写一些进程相关的shell命令，打包失败，一般是使用 -F 可以成功，但是执行exe时有cmd弹窗，这非常不美观， 如果使用-Fw c参数执行exe 直接失败。 这种情况有两种解决方案。

方案一： 使用 pyinstaller -Dw file.py 生成的是一个目录文件。 程序执行成功，无黑名终端弹窗情况。

方案二： 起用 os.popen()  方法， 改用subprocess.Popen() 模块

​	下面是我的测试，亲测成功， 参数一定要配置好，否则程序执行失败！

```python
import subprocess
def checkprocess():
    processnames = ['EXCEL.EXE']
    for processname in processnames:
        p = subprocess.Popen('taskkill /F /IM %s' %processname,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        p.wait()
checkprocess()
```



有空写一个 关于subprocess的教程，详细研究一下他的参数配置





​	参考 ：<https://blog.csdn.net/hpwzjz/article/details/82992176>  