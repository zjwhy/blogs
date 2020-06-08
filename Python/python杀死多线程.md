# Python杀死子线程

```
import threading
import time
import inspect
import ctypes


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def print_time():
    while 2:
        print("子线程")
        time.sleep(3)


if __name__ == "__main__":
    t = threading.Thread(target=print_time)
    t.start()


    print("stoped")
    while 1:
        time.sleep(3)
        print(threading.active_count())
        print("时间", time.localtime().tm_sec % 10 > 9)
        if time.localtime().tm_sec % 10 > 9:
            stop_thread(t)

        pass
```