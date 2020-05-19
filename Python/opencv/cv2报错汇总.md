# cv2报错汇总

## cv2打开中文路径文件报错

```
# 灰度读取
im = cv2.imdecode(np.fromfile(targetpath, dtype=np.uint8), 0)
```

