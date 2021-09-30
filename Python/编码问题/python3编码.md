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

# 重定向管道输出编码格式

```
def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if '\u3000' <= ch <= u'\u9fff':
            return True


class RPAPrint():
    def __init__(self):
        self.buff = ""
        self.__console__ = sys.stdout

    def write(self, output_string):
        if check_contain_chinese(output_string.encode()):
            self.__console__.write(output_string.encode("unicode_escape").decode('utf-8'))
        else:
            self.__console__.write(output_string)

    def flush(self):
        self.__console__.flush()

    def reset(self):
        sys.stdout = self.__console__


sys.stdout = RPAPrint()
```

# **更改标准流的编码**

[参考网址](https://www.cnpython.com/qa/35467)

```
sys.stdout.reconfigure(encoding='utf-8')

# 示例
import sys
sys.stdout.reconfigure(encoding='gbk',errors ='replace')
```

