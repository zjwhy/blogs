# 设置焦点报错

```python
def set_focus(self):
    """
    设置焦点，存在没有权限问题
    https://stackoverflow.com/questions/62649124/pywin32-setfocus-resulting-in-access-is-denied-error
    """
    remote_thread, _ = win32process.GetWindowThreadProcessId(self.hwnd)
    win32process.AttachThreadInput(win32api.GetCurrentThreadId(), remote_thread, True)
    return win32gui.SetFocus(self.hwnd)
```

