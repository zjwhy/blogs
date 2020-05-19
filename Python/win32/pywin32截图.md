# 代码

```
import win32gui
import win32ui
import win32con
import win32api


def window_capture(filename, wmin, hmin, wmax, hmax):
    hwnd = 0 #Desktop
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    BitMap = win32ui.CreateBitmap()
    BitMap.CreateCompatibleBitmap(mfcDC, wmax-wmin, hmax-hmin)
    saveDC.SelectObject(BitMap)
    saveDC.BitBlt((0, 0), (wmax, hmax), mfcDC, (wmin, hmin), win32con.SRCCOPY)
    BitMap.SaveBitmapFile(saveDC, filename)

    win32gui.DeleteObject(BitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
```

# bmip转base64的jpeg

```
import win32gui
import win32ui
import win32con
import win32api
from PIL import Image
from io import BytesIO
def window_capture(filename, wmin, hmin, wmax, hmax):
    hwnd = 0 #Desktop
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    BitMap = win32ui.CreateBitmap()
    BitMap.CreateCompatibleBitmap(mfcDC, wmax-wmin, hmax-hmin)
    saveDC.SelectObject(BitMap)
    saveDC.BitBlt((0, 0), (wmax, hmax), mfcDC, (wmin, hmin), win32con.SRCCOPY)

    bmpinfo = BitMap.GetInfo()
    bmpstr = BitMap.GetBitmapBits(True)
    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    output_buffer = BytesIO()
    im.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    print('data:image/1.jpeg;base64,%s' % base64_str.decode())
    # im.save("test.png")

    # BitMap.SaveBitmapFile(saveDC, filename)

    win32gui.DeleteObject(BitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
window_capture('1.png', 0,0,100,100)
```

[https://www.jianshu.com/p/2ff8e6f98257](PIL.Image与Base64 String的互相转换)

[https://www.cnblogs.com/strive-sun/p/12050061.html](使用python获得屏幕截图并保存为位图文件)

