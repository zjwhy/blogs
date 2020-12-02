# -*- coding: utf-8 -*-
'''
RPA 对字符串的处理
'''


def replace(string, old, new, count = None):
    '''
    replace(string,old, new[, count]) -> str
    
        功能：将source字符串中的old字符串替换为new字符串，最多替换count次, count未定义则全部替换
    
        参数:
        string: 被替换的源字符串.
        old   : 需要被替换的字符串.
        new   : 需要替换成的字符串.
        count : 替换次数，默认全部.

        返回:
                替换后的字符串.
        例子:
        replace('abc', 'a', 'd') -> 'dbc'

    '''
    if(count != None):
         return string.replace(old,new,count)
    else:
         return string.replace(old,new)


def capitalize(string):
    '''
    capitalize(string) -> str
        功能：将字符串的第一个字符转换为大写
        参数：
        string: 被替换的源字符串.

        返回:
               返回一个首字母大写的字符串
        例子:
        capitalize('abc') -> 'Abc'

    '''
    return string.capitalize()


def count(string,sub, start=None, end=None):
    '''
    count(string,sub[, start[, end]]) -> int
        功能：返回sub在字符串string里面出现的次数，如果 start 或者 end 指定则返回指定范围内出现sub的次数
        参数：
        string: 字符串
        sub:  搜索的子字符串。
        start: 字符串开始搜索的位置。默认为第一个字符,第一个字符索引值为0。
        end : 字符串中结束搜索的位置。字符中第一个字符的索引为 0。默认为字符串的最后一个位置。

        返回:
               返回子字符串在字符串中出现的次数。
        例子:
        count('abc','a') ->1


    '''
    return string.count(sub, start, end)


def encode(string,encoding='utf-8', errors='strict'):
    '''
    encode(string,encoding='utf-8', errors='strict') -> bytes

        功能：以 encoding 指定的编码格式编码字符串，如果出错默认报一个ValueError 的异常，除非 errors 指定的是'ignore'或者'replace'

        参数：
        string: 要编码字符串
        encoding:  要使用的编码，如: UTF-8。
        errors: 设置不同错误的处理方案。默认为 'strict',意为编码错误引起一个UnicodeError。 其他可能得值有 'ignore', 'replace',
                'xmlcharrefreplace', 'backslashreplace' 以及通过 codecs.register_error() 注册的任何值。

        返回:
              返回编码后的字符串，它是一个 bytes 对象。
        例子:
        encode('abc') ->b'abc'


    '''
    return string.encode(encoding, errors)


def endswith(string,suffix, start=None, end=None):
    '''
    endswith(string,suffix[, start[, end]]) -> bool
        功能：检查字符串是否以suffix结束，如果start或者 end 指定则检查指定的范围内是否以 obj 结束，如果是，返回 True,否则返回 False.

        参数：
        string: 待检查的字符串
        suffix : 该参数可以是一个字符串或者是一个元素。
        start : 字符串中的开始位置。
        end : 字符串中结束位置。

        返回:
              如果字符串含有指定的后缀返回True，否则返回False。
        例子:
        endswith('abc','c') ->True
    '''
    return string.endswith(suffix, start, end)


def startswith(string, prefix, start=None, end=None):
    '''
    startswith(prefix[, start[, end]]) -> bool
        功能：检查string字符串是否是以指定子字符串开头，如果是则返回 True，否则返回 False。如果参数 beg 和 end 指定值，则在指定范围内检查。

        参数：
        string: 待检查的字符串
        prefix : 检测的字符串
        start : 字符串中的开始位置。
        end : 字符串中结束位置。

        返回:
              如果检测到字符串则返回True，否则返回False。
        例子:
        startswith('abc','a') ->True
    '''
    return string.startswith(prefix, start, end)



def find(string, sub, start=None, end=None):
    '''
    find(string,sub[, start[, end]]) -> int
        功能：检测 sub 是否包含在字符串中，如果指定范围 start 和 end ，则检查是否包含在指定范围内，如果包含返回开始的索引值，否则返回-1

        参数：
        string: 待检查的字符串
        sub: 指定检索的字符串
        start : 开始索引，默认为0。
        end : 结束索引，默认为字符串的长度。

        返回:
              如果包含子字符串返回开始的索引值，否则返回-1。
        例子:
        find('abc','c') ->2
    '''
    return string.find(sub, start, end)


def isdigit(string):
    '''
    isdigit(string) -> bool
        功能：如果字符串只包含数字则返回 True 否则返回 False.

        参数：
        string: 待检查的字符串

        返回:
              如果字符串只包含数字则返回 True 否则返回 False。
        例子:
        isdigit('1111111') ->True
    '''
    return string.isdigit()


def islower(string):
    '''
    islower(string) -> bool
        功能：检测字符串中所有的字母是否都为小写。

        参数：
        string: 待检查的字符串

        返回:
              如果字符串中包含至少一个区分大小写的字符，并且所有这些(区分大小写的)字符都是小写，则返回 True，否则返回 False
        例子:
        islower('aaaaa') ->True
    '''
    return string.islower()

def isupper(string):
    '''
    isupper(string) -> bool
        功能：检测字符串中所有的字母是否都为大写。

        参数：
        string: 待检查的字符串

        返回:
              如果字符串中包含至少一个区分大小写的字符，并且所有这些(区分大小写的)字符都是大写，则返回 True，否则返回 False
        例子:
        isupper('AAAAA') ->True
    '''
    return string.isupper()


def isnumeric(string):
    '''
    isnumeric() -> bool
         功能：检测字符串中是否只包含数字字符

        参数：
        string: 待检查的字符串

        返回:
              如果字符串中只包含数字字符，则返回 True，否则返回 False
        例子:
        isnumeric('1111') ->True
    '''
    return string.isnumeric()

def isspace(string):
    '''
    isspace(string) -> bool
        功能：检测字符串是否只由空白字符组成。

        参数：
           string: 待检查的字符串
        返回:
              如果字符串中只包含空格，则返回 True，否则返回 False.
        例子:
        isspace(' ') ->True


    '''
    return string.isspace()

def join(string,iterable):
    '''
    join(string,iterable) -> str
        功能：将序列中的元素以指定的字符连接生成一个新的字符串.

        参数：
          string :待处理字符串
          iterable :要连接的元素序列。
        返回:
            返回通过指定字符连接序列中元素后生成的新字符串。
        例子:
        join(' ',("aa","bb","cc")) ->aa bb cc


    '''
    return string.join(iterable)


def len_str(string):
    '''
    len(string) -> int
        功能：返回对象（字符、列表、元组等）长度或项目个数。
        参数：
          string :待处理字符串
        返回:
            返回对象长度。
        例子:
        len_str('abd') ->3

    '''
    return len(string)


def lstrip(string, chars=None):
    '''
    lstrip(string[,chars]) -> str
        功能：截掉字符串左边的空格或指定字符。

        参数：
          string :待处理字符串
          chars :指定截取的字符
        返回:
            返回截掉字符串左边的空格或指定字符后生成的新字符串。
        例子:
        lstrip('asada','a') ->sada

    '''
    return string.lstrip(chars)

def rstrip(string, chars=None):
    '''
    rstrip(string[,chars]) -> str
        功能： 删除 string 字符串末尾的指定字符（默认为空格）.

        参数：
          string :待处理字符串
          chars :指定截取的字符
        返回:
            返回删除 string 字符串末尾的指定字符后生成的新字符串。
        例子:
        rstrip('asada','a') ->asad

    '''
    return string.rstrip(chars)




def maketrans(string, outstring):
    '''
    maketrans(string, outstring) -> dict
        功能：创建字符映射的转换表
        参数：
            string ： 字符串中要替代的字符组成的字符串。
            outstring ： 相应的映射字符的字符串。
        返回：
            返回字符串对应的翻译表。
        例子：
           maketrans('123', 'abc') ->{49: 97, 50: 98, 51: 99}

    '''
    return str.maketrans(string,outstring)

def translate(string,table):
    '''
    translate(string,table) -> str
        功能：根据翻译表(包含 256 个字符)转换字符串的字符,要过滤掉的字符放到 deletechars 参数中
        参数：
            string:需要翻译的字符串
            table :翻译表，翻译表是通过 maketrans()方法转换而来。
        返回：
            返回翻译后的字符串
        例子：
           translate('2334411',maketrans('123', 'abc')) ->bcc44aa

    '''
    return string.translate(table)

def max_str(string):
    '''
    max(string) -> str
        功能：返回字符串中最大的字母
        参数：
            string:需要处理的字符串

        返回：
            返回字符串中最大的字母
        例子：
           max_str('abcxz')->z

    '''
    return max(string)

def min_str(string):
    '''
    min(string) -> str
        功能：返回字符串中最小的字母
        参数：
            string:需要处理的字符串

        返回：
            返回字符串中最小的字母
        例子：
           min_str('abcxz')->a

    '''
    return min(string)

def rfind(string, sub, start=None, end=None):
    '''
    rfind(string,sub[, start[, end]]) -> int
        功能：类似于 find()函数，不过是从右边开始查找.
        参数：
            string:需要检索的字符串
            sub: 指定检索的字符串
            start : 开始索引，默认为0。
            end : 结束索引，默认为字符串的长度。

        返回:
              如果包含子字符串返回开始的索引值，否则返回-1。
        例子:
           rfind('abc','c') ->0

    '''
    return string.rfind(sub, start, end)

def rjust(string, width, fillchar=None):
    '''
    rjust(string,width[, fillchar]) -> str
        功能：返回一个原字符串右对齐,并使用空格填充至长度 width 的新字符串。如果指定的长度小于字符串的长度则返回原字符串。
        参数：
            string:字符串
            width: 指定填充指定字符后中字符串的总长度.
            fillchar : 填充的字符，默认为空格.

        返回:
             返回一个原字符串右对齐,并使用空格填充至长度 width 的新字符串。如果指定的长度小于字符串的长度则返回原字符串
        例子:
           rjust('abc',10,,'$') ->$$$$$$$abc

    '''
    if fillchar!=None:
        return string.rjust(width, fillchar)
    else:
        return string.rjust(width)

def split(string,str=None,num=None):
    '''
    split(string,str,num) -> list of strings
         功能：通过指定分隔符对字符串进行切片，如果参数num 有指定值，则仅分隔 num 个子字符串
         参数：
             string:字符串
             str : 分隔符，默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等。
             num : 分割次数。
         返回:
             返回分割后的字符串列表。
         例子:
           split('abcabcab','c',1) ->['ab', 'abcab']

    '''
    if num!=None:
        return string.split(str,num)
    else:
        if str==None:
            return string.split()
        else:
            return string.split(str)

def strip(string, chars=None):
    '''
    strip([chars]) -> str
         功能：移除字符串头尾指定的字符（默认为空格）。
         参数：
             string:字符串
             chars :  移除字符串头尾指定的字符。
         返回:
             返回移除字符串头尾指定的字符生成的新字符串。
         例子:
            strip('**abcabcab**','*') -> abcabcab

    '''
    return string.strip(chars)

def swapcase(string):
    '''
    swapcase() -> str
         功能：对字符串的大小写字母进行转换。
         参数：
             string:字符串
         返回:
             返回大小写字母转换后生成的新字符串。
         例子:
            swapcase('abAB') ->ABab

    '''
    return string.swapcase()

def upper(string):
    '''
    upper() -> str
         功能：字符串中的小写字母转为大写字母
         参数：
             string:字符串
         返回:
             返回转换后生成的新字符串。
         例子:
            upper('abAB') ->ABAB

    '''
    return string.upper()

def lower(string):
    '''
    lower() -> str
         功能：字符串中所有大写字符转换为小写。
         参数：
             string:字符串
         返回:
             返回转换后生成的新字符串。
         例子:
            lower('abAB') ->abab

    '''
    return string.lower()

def iprint(param):
    '''
    :param param:
    :return:  打印内容
    '''
    print(param)


def zfill(string, width):
    '''
        zfill() -> str
             功能：返回指定长度的字符串，原字符串右对齐，前面填充0。
             参数：
                 string:字符串
                 width :指定长度
             返回:
                 返回转换后生成的新字符串。
             例子:
                '12345'.zfill(10) ->'0000012345'

        '''
    return string.zfill(width)
