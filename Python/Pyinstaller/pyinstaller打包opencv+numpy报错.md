# 报错背景
	这两天公司的程序许需要打包，就开始又操作了一番。
	pyinstller 打包含有opencv+numpy库 打包成功，但是运行报错。在排除外部依赖文件因素外，看了一下运行结果。


```python
ImportError: numpy.core.multiarray failed to import
```

# 解决方案
	重要的是pycharm运行正常，cmd运行正常，只有打包程序异常。经过查阅决定从版本问题解决，亲测打包后成功运行。
	
	一般情况下是由于numpy版本过高导致的，因为我看了源码是有  numpy.core.multiarray这个部分代码的


​	
	经过测试找出对应版本：
	opencv -- 3.4.5.20 
	numpy  --1.16.4
	python --3.68