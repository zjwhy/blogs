# 背景

项目上同事在做编辑器，我在想能不能用python仿一个cmd，然后嵌入到编辑器中，首先想到了subprocess库，经过长时间的测试，终于测试出一个比较有意思的cmd（目前还不能像cmd一样使用环境变量的命令）



# 实现

**主要是用多线程，一个负责读取，一个负责写入**

```
import base64
import os
import time
from subprocess import *
import threading

tag = 0
# p = Popen(r"python D:\Desktop\Msxf\rpa\python\spy++\test.py",stdin=PIPE,stdout=PIPE, stderr=STDOUT, shell=True)
p = Popen(r"cmd.exe",stdin=PIPE,stdout=PIPE, stderr=STDOUT, shell=True)

def out():
    global p
    while 1:
            if p.poll() != None:
                print('检测子进程结束')
                break
            line = p.stdout.readline().strip()
            # if line != b'':
            #     print(line.decode('GBK'))
            print(line.decode('GBK'))

def inp():
    global tag
    global p
    while 1:
        time.sleep(1)
        if tag == 0:
            data = input("%s>" % os.getcwd()) + '\r\n'
            p.stdin.write(data.encode('GBK'))
            p.stdin.flush()
            # tag = 1

out_t = threading.Thread(target=out)
inp_t = threading.Thread(target=inp)
inp_t.start()
out_t.start()

out_t.join()
inp_t.join()

```

