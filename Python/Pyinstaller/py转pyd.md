# Py文件打包为pyd

## 优点

1. 速度快
2. 不可反编译

## 缺点

1. 不支持跨python版本
2. 不支持跨平台
3. 不可读

## 代码示例

```python
"""
@fileName: setup.py
"""
from distutils.core import setup, run_setup
from Cython.Build import cythonize
from distutils.extension import Extension

 setup(name='mBot',
              version='1.0',
              description='RPA 测试打包',
              author='yunsheng.bi',
              author_email='rpa@msxf.com',
              url='https://www.python.org/sigs/distutils-sig/',
              packages=['mBot'],
              ext_modules=cythonize(self.files, build_dir=self.buildDirPath)
              )
```

```
python.exe setup.py build_ext
```

[1]: https://www.python.org/sigs/distutils-sig/	"distutils"



