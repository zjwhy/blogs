# 驱动下载路径

[chromedriver](http://selenium-release.storage.googleapis.com/index.html)

# chromedriver设置下载路径

在下载文件时如果不设置下载路径，这种情况就会弹出一个windows弹窗让你选在下载路径，假如是人操作无所谓，但是要是进行自动化操作那种比较麻烦了，还要通过控制windows窗体设置下载路径。

但是对于selenium只需要简单的设置一个chrome_options参数就ok了

```python
from selenium import webdriver
options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': r'd:\'}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options=options)
driver.maximize_window()
driver.get(r'测试url')
```

profile.default_content_settings.popups:0 禁止弹出窗口

download.default_directory 设置下载位置

