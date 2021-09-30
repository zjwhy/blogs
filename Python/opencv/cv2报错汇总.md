# cv2报错汇总

## cv2打开中文路径文件报错

```
# 灰度读取
im = cv2.imdecode(np.fromfile(targetpath, dtype=np.uint8), 0)
```

# win7纯净系统安装cv2报错 importerror dll

1、安装vc2015

https://www.microsoft.com/en-us/download/details.aspx?id=48145

2、复制dll文件

api-ms-win-downlevel-shlwapi-l1-1-0.dll

https://www.dll-files.com/api-ms-win-downlevel-shlwapi-l1-1-0.dll.html