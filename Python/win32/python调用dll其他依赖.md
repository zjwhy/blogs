# python调用dll，自定义依赖路径

```
# 设置dll的依赖项路径
win32api.SetDllDirectory('ie')
# 加载动态dll
ctypes.cdll.LoadLibrary('ie/RPA_IE_Plugin.dll')
```

