# python asyncio

## 问题

1. **[解决async 运行多线程时报错RuntimeError: There is no current event loop in thread 'Thread-2'](https://www.cnblogs.com/SunshineKimi/p/12053914.html)**

```
单线程使用时：
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(do_work(checker))
loop.run_until_complete(asyncio.wait([task]))
st = task.result()

多线程获取新的loop，并且设置loop
new_loop = asyncio.new_event_loop()
asyncio.set_event_loop(new_loop)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(do_work(checker))
loop.run_until_complete(asyncio.wait([task]))
st = task.result()
```

```
asyncio get_event_loop源代码

def get_event_loop(self):
    """Get the event loop.
    This may be None or an instance of EventLoop.
    """
    if (self._local._loop is None and
            not self._local._set_called and
            isinstance(threading.current_thread(), threading._MainThread)):
        self.set_event_loop(self.new_event_loop())
 
    if self._local._loop is None:
        raise RuntimeError('There is no current event loop in thread %r.'
                            % threading.current_thread().name)
 
    return self._local._loop
    
在主线程中，调用get_event_loop总能返回属于主线程的event loop对象，如果是处于非主线程中，还需要调用set_event_loop方法指定一个event loop对象，这样get_event_loop才会获取到被标记的event loop对象：


```

[https://docs.python.org/zh-cn/3/library/asyncio-eventloop.html]: 
[https://segmentfault.com/q/1010000015292636]: 

## 解决 `RuntimeError: This event loop is already running`

[https://github.com/erdewit/nest_asyncio]: 

```
pip3 install nest_asyncio
```

```
import nest_asyncio
nest_asyncio.apply()
```

