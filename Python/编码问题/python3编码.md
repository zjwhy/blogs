# 关于python3编码问题汇总

## 编码官方文档

[1]: https://docs.python.org/3/library/codecs.html?highlight=surrogateescape#encodings-and-unicode	"python3.7自定义编码器官方文档"



## 获取当前编码api

[1]: https://docs.python.org/zh-cn/3.7/library/locale.html?highlight=locale%20getpreferredencoding#locale.getpreferredencoding	"import locale locale.getdefaultlocale"



```
locale.getdefaultlocale([envvars])
Tries to determine the default locale settings and returns them as a tuple of the form (language code, encoding).

According to POSIX, a program which has not called setlocale(LC_ALL, '') runs using the portable 'C' locale. Calling setlocale(LC_ALL, '') lets it use the default locale as defined by the LANG variable. Since we do not want to interfere with the current locale setting we thus emulate the behavior in the way described above.

To maintain compatibility with other platforms, not only the LANG variable is tested, but a list of variables given as envvars parameter. The first found to be defined will be used. envvars defaults to the search path used in GNU gettext; it must always contain the variable name 'LANG'. The GNU gettext search path contains 'LC_ALL', 'LC_CTYPE', 'LANG' and 'LANGUAGE', in that order.

Except for the code 'C', the language code corresponds to RFC 1766. language code and encoding may be None if their values cannot be determined.
```

[2]: https://docs.python.org/zh-cn/3.7/library/sys.html?highlight=sys%20getdefaultencoding#sys.getdefaultencoding	"import sys sys.getdefaultencoding()"

```
sys.getdefaultencoding()
返回当前 Unicode 实现所使用的默认字符串编码名称。
```

