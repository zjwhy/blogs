# PIL系统截图、cv2图片匹配

```python
from PIL import ImageGrab
import cv2
import numpy as np

from utils.windows import mouseMove, mouseClick


def mathc_img(Target, value = 0.9):
    try:
        im = np.array(ImageGrab.grab())
        img_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(Target, 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = value
        loc = np.where(res >= threshold)
        return (int(loc[1][0]), int(loc[0][0]))
    except :
        raise Exception('未匹配到图片')


def imageSearchClick(Target, x_, y_):
    mouseMove(0, 0)
    x, y = mathc_img(Target)
    mouseMove(x + x_, y + y_)
    mouseClick()
    mouseMove(0, 0)



if __name__ == '__main__':
    # x, y = mathc_img(r'C:\Users\btc\Desktop\1.PNG')
    # mouseMove(x, y)
    imageSearchClick(r'C:\invoicePrint\images\tool0.PNG', 50, 30)

```

其中的 mouseClick和mouseMove是我自己定义的操作鼠标函数，采用pywin32写的