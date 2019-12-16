

# PostMessage（）

```python
def keyHwnd(hwndEx, char):
    """
    向指定控件输入值
    :param hwndEx: 控件句柄
    :param char: 字符串
    :return: True or Flase
    """
    try:
        for _ in char:
            print('key:%s    ascii:%d'  % (_, ord(_)))
            win32api.PostMessage(hwndEx, win32con.WM_CHAR, ord(_), 0)
            time.sleep(random.uniform(0,0.2))
    except Exception as e:
        print(e)
        return False

    return True
    
hwnd = win32gui.FindWindow(None,'a.txt - 记事本')
print(hwnd)

win32gui.SetForegroundWindow(hwnd)
hwndex = win32gui.FindWindowEx(hwnd,None,'Edit', None)
keyHwnd(hwndex,'撒地方SDFkof;ldsojfdfdsjfd;slkjfdlksjfkldsjflkdsjlkfjkldsljkfjdssj')
   
```





# 切换键盘布局

**该功能封装成了一个装饰器，函数执行完恢复了原键盘布局**

```python
import win32con
from win32con import WM_INPUTLANGCHANGEREQUEST
import win32gui
import win32api

def setKeyboardLayout_en(inner):

    def wrapper(*args, **kwargs):
        if win32api.LoadKeyboardLayout('0x0409', win32con.KLF_ACTIVATE) == None:
            return Exception('加载键盘失败')
        # 语言代码
        # https://msdn.microsoft.com/en-us/library/cc233982.aspx
        LID = {0x0804: "Chinese (Simplified) (People's Republic of China)",
               0x0409: 'English (United States)'}

        # 获取前景窗口句柄
        hwnd = win32gui.GetForegroundWindow()

        # 获取前景窗口标题
        title = win32gui.GetWindowText(hwnd)
        # 获取键盘布局列表
        im_list = win32api.GetKeyboardLayoutList()
        im_list = list(map(hex, im_list))
        print(im_list)
        oldKey = hex(win32api.GetKeyboardLayout())

        # 设置键盘布局为英文
        result = win32api.SendMessage(
            hwnd,
            WM_INPUTLANGCHANGEREQUEST,
            0,
            0x4090409)
        if result == 0:
            print('设置英文键盘成功！')


        inner(*args,*kwargs)

        result = win32api.SendMessage(
            hwnd,
            WM_INPUTLANGCHANGEREQUEST,
            0,
            oldKey)
        if result == 0:
            print('还原键盘成功！')
    return wrapper


```



# ascii标准码

![ascii标准码](https://img2018.cnblogs.com/blog/1600965/201906/1600965-20190604095902019-2130233897.png)



# keybd_event()

```python
win32api.keybd_event(65, 0, 0, 0)
time.sleep(random.uniform(0, 0.5))
win32api.keybd_event(65, 0, win32con.KEYEVENTF_KEYUP, 0)
```



[microsoft键盘码参考](https://docs.microsoft.com/zh-cn/windows/desktop/inputdev/virtual-key-codes)



![](https://img-bbs.csdn.net/upload/201407/18/1405648879_285726.jpg)

![](https://img-bbs.csdn.net/upload/201407/18/1405648891_822255.jpg)





[**这位兄弟写的关于模拟键盘非常全**](https://bbs.csdn.net/topics/90509805)

