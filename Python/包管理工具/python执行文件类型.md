# python可执行文件类型及说明

1. py 源代码文件
2. pyc 字节码文件
3. pyd D语言编写的动态文件,可通过cython将py转为pyd
4. pyw 隐藏gui执行
5. zip 若压缩包里有 __ mai __.py,可直接执行模块
6. pyo 优化后的字节文件， 通过python -o 可生成

# pyc逆向示例

```
# -*- encoding: utf-8 -*-

"""
@Author  :   biyunsheng
@License :   (C) Copyright 2013-2020, msxf
@Software:   PyCharm
@File    :   2.py
@Time    :   2021/4/27
"""
import asyncio
import os

import uncompyle6
import time


class UnCompyle:
    def __init__(self, pycFile, pyPath="out.py"):
        self.pycFile = pycFile
        self.pyPath = pyPath

    def uncompy(self):
        with open(self.pyPath, 'w', encoding="utf-8") as f:
            uncompyle6.decompile_file(self.pycFile, f)


class Traverse:
    def __init__(self):
        pass

    def recursionDir(self, filePath):
        if os.path.isfile(filePath):
            ileDirName, fileName = os.path.split(filePath)
            filePathName, extendName = os.path.splitext(filePath)
            if extendName == ".pyc":
                outPyFilePath = os.path.join(filePathName + ".py")
                print(outPyFilePath)
                uncompyle = UnCompyle(pycFile, outPyFilePath)
                uncompyle.uncompy()
                del uncompyle
                os.remove(filePath)
            else:
                pass
        else:
            for name in os.listdir(filePath):
                newPath = os.path.join(filePath, name)
                self.recursionDir(newPath)
if __name__ == '__main__':
    pycFile = r'D:\Huawei\WeAutomate\Studio 2.14.0\Robot\antrobot.pyc'
    pycDirPath = r'E:\Desktop\blogs\RPA\组件\Robot'
    UnCompyle(pycFile).uncompy()
    Traverse().recursionDir(pycDirPath)
```

# py转pyd

```
import os
import shutil
from distutils.core import setup, run_setup
from Cython.Build import cythonize
from distutils.extension import Extension
"""
注意事项：
    1、pyd不支持跨python版本
    2、启动命令 python.exe setup.py build_ext

"""

class ComplePy2Pyd:
    """
    py2pyd
    """

    def __init__(self, dirPath):
        """
        :param dirPath:
        """
        self.dirPath = dirPath
        self.buildDirPath = "build\lib"
        self.libDirPath = "build\lib.win32-3.7"
        self.files = []
        self.initialization()
        self.getAllPy()

    def initialization(self):
        shutil.rmtree("build")

    def getAllPy(self):
        for root, dirs, files in os.walk(self.dirPath):
            for file in files:
                fileName, extendName = os.path.splitext(file)

                # 文件路径
                filePath = os.path.join(root, file)

                # 判读是否为py文件 且不为 __init__.py
                if extendName == ".py" and file != "__init__.py":
                    self.files.append(filePath)
                else:
                    targetDirPath = os.path.join(self.libDirPath, root)
                    targetFilePath = os.path.join(self.libDirPath, filePath)
                    os.makedirs(targetDirPath, exist_ok=True)
                    shutil.copyfile(filePath, targetFilePath)

    def setUp(self):
        setup(name='Distutils',
              version='1.0',
              description='RPA 测试打包',
              author='yunsheng.bi',
              author_email='rpa@msxf.com',
              url='https://www.python.org/sigs/distutils-sig/',
              packages=['helloRPA'],
              ext_modules=cythonize(self.files, build_dir=self.buildDirPath)
              )


if __name__ == '__main__':
    file = r'E:\Desktop\RPAWork\CSEditorPython\trunk\compentsAdministration\mBot'
    comp = ComplePy2Pyd('mBot')
    comp.setUp()
```