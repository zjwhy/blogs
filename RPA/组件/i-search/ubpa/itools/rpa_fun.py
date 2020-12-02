# -*- coding: utf-8 -*-
'''
RPA 对正则表达式的处理
    数学函数处理，及 随机数处理
'''
import re
import math
import random
from ubpa.ilog import ILog
__logger = ILog(__file__)


def lens(param):
    '''
        len(param) -> int
            功能：返回对象（字符、列表、元组等）长度或项目个数。
            参数：
              param :待处理的对象
            返回:
                返回对象长度。
            例子:
            len('abd')          -> 3
            len([1,2,3,4])      -> 4
            len((1,2,3,4,5))    -> 5
        '''
    __logger.echo_msg(u"ready to execute[lens]")
    try:
        return len(param)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[lens]")


def match(pattern, string, flags=0):
    '''
        match(pattern, string, flags=0) -> 匹配的对象 or None

            功能：re.match 尝试从字符串的起始位置匹配一个模式，如果不是起始位置匹配成功的话，match()就返回none

            参数:
            pattern : 匹配的正则表达式.
            string  : 要匹配的字符串.
            flags   : 标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等.
                      re.I	使匹配对大小写不敏感
                      re.L	做本地化识别（locale-aware）匹配
                      re.M	多行匹配，影响 ^ 和 $
                      re.S	使 . 匹配包括换行在内的所有字符
                      re.U	根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B.
                      re.X	该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解。
            返回:
                    返回一个匹配的对象，否则返回None.
            例子:
            re.match('www', 'www.runoob.com').span() -> (0, 3)     # 在起始位置匹配
            re.match('com', 'www.runoob.com') -> None         # 不在起始位置匹配

        '''
    __logger.echo_msg(u"ready to execute[match]")
    try:
        return re.match(pattern, string, flags=flags)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[match]")


def search(pattern, string, flags=0):
    '''
            search(pattern, string, flags=0) -> 匹配的对象 or None

                功能：search 扫描整个字符串并返回第一个成功的匹配

                参数:
                pattern : 匹配的正则表达式.
                string  : 要匹配的字符串.
                flags   : 标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等.
                          re.I	使匹配对大小写不敏感
                          re.L	做本地化识别（locale-aware）匹配
                          re.M	多行匹配，影响 ^ 和 $
                          re.S	使 . 匹配包括换行在内的所有字符
                          re.U	根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B.
                          re.X	该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解。
                返回:
                        返回一个匹配的对象，否则返回None.
                例子:
                re.match('www', 'www.runoob.com').span() -> (0, 3)     # 在起始位置匹配
                re.match('com', 'www.runoob.com') -> (11, 14)         # 不在起始位置匹配

            '''
    __logger.echo_msg(u"ready to execute[search]")
    try:
        return re.search(pattern, string, flags=flags)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[search]")


def sub(pattern, repl, string, count=0):
    '''
            sub(pattern, repl, string, count=0) -> str

                功能：sub 用于替换字符串中的匹配项

                参数:
                pattern : 正则中的模式字符串。
                repl : 替换的字符串，也可为一个函数。
                string : 要被查找替换的原始字符串。
                count : 模式匹配后替换的最大次数，默认 0 表示替换所有的匹配。

                返回:
                        返回被替换后的字符串
                例子:
                phone = "2004-959-559 # 这是一个电话号码"
                num = sub(r'#.*$', "", phone)
                num ->  2004-959-559     # 删除注释

                num = re.sub(r'\D', "", phone)
                num ->  2004959559    # 移除非数字的内容

                repl 参数是一个函数
                def double(matched):
                    value = int(matched.group('value'))
                    return str(value * 2)

                s = 'A23G4HFD567'
                result = sub('(?P<value>\d+)', double, s)
                result ->  A46G8HFD1134     # 将匹配的数字乘于 2
               '''
    __logger.echo_msg(u"ready to execute[sub]")
    try:
        return re.sub(pattern, repl, string, count=count)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[sub]")


def re_case_sensitive(pattern, string):
    '''
            re_case_sensitive(pattern, string) -> 匹配的对象 or None

                功能：search 扫描整个字符串并返回第一个成功的匹配
                参数:
                pattern : 匹配的正则表达式.
                string  : 要匹配的字符串.
                flags   : 标志位，用于控制正则表达式的匹配方式
                          re.I	使匹配对大小写不敏感
                返回:
                        返回一个匹配的对象，否则返回None.
                例子:
                re_case_sensitive('www', 'www.runoob.com').span() -> (0, 3)     # 在起始位置匹配
                re_case_sensitive('com', 'www.runoob.com') -> (11, 14)         # 不在起始位置匹配

            '''
    __logger.echo_msg(u"ready to execute[re_case_sensitive]")
    try:
        return re.search(pattern, string, flags=re.I)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[re_case_sensitive]")


def re_line_breaks(pattern, string):
    '''
            re_line_breaks(pattern, string) -> 匹配的对象 or None

                功能：search 扫描整个字符串并返回第一个成功的匹配

                参数:
                pattern : 匹配的正则表达式.
                string  : 要匹配的字符串.
                flags   : 标志位，用于控制正则表达式的匹配方式
                          re.S	设置匹配换行
                返回:
                        返回一个匹配的对象，否则返回None.
                例子:
                re_line_breaks('www', 'www.runoob.com').span() -> (0, 3)     # 在起始位置匹配
                re_line_breaks('com', 'www.runoob.com') -> (11, 14)         # 不在起始位置匹配
            '''
    __logger.echo_msg(u"ready to execute[re_line_breaks]")
    try:
        return re.search(pattern, string, flags=re.S)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[re_line_breaks]")


def re_localization(pattern, string):
    '''
            search(pattern, string) -> 匹配的对象 or None

                功能：search 扫描整个字符串并返回第一个成功的匹配

                参数:
                pattern : 匹配的正则表达式.
                string  : 要匹配的字符串.
                flags   : 标志位，用于控制正则表达式的匹配方式
                          re.L	设置本地化识别
                返回:
                        返回一个匹配的对象，否则返回None.
                例子:
                re_localization('www', 'www.runoob.com').span() -> (0, 3)     # 在起始位置匹配
                re_localization('com', 'www.runoob.com') -> (11, 14)         # 不在起始位置匹配

            '''
    __logger.echo_msg(u"ready to execute[re_localization]")
    try:
        return re.search(pattern, string, flags=re.L)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[re_localization]")


def re_multi_line(pattern, string):
    '''
            re_multi_line(pattern, string) -> 匹配的对象 or None

                功能：search 扫描整个字符串并返回第一个成功的匹配

                参数:
                pattern : 匹配的正则表达式.
                string  : 要匹配的字符串.
                flags   : 标志位，用于控制正则表达式的匹配方式
                          re.M	设置多行匹配
                返回:
                        返回一个匹配的对象，否则返回None.
                例子:
                re_multi_line('www', 'www.runoob.com').span() -> (0, 3)     # 在起始位置匹配
                re_multi_line('com', 'www.runoob.com') -> (11, 14)         # 不在起始位置匹配

            '''
    __logger.echo_msg(u"ready to execute[re_multi_line]")
    try:
        return re.search(pattern, string, flags=re.M)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[re_multi_line]")


def re_flexible(pattern, string):
    '''
                re_flexible(pattern, string) -> 匹配的对象 or None

                    功能：search 扫描整个字符串并返回第一个成功的匹配

                    参数:
                    pattern : 匹配的正则表达式.
                    string  : 要匹配的字符串.
                    flags   : 标志位，用于控制正则表达式的匹配方式
                             re.X  设置更灵活的格式
                    返回:
                            返回一个匹配的对象，否则返回None.
                    例子:
                    re_flexible('www', 'www.runoob.com').span() -> (0, 3)     # 在起始位置匹配
                    re_flexible('com', 'www.runoob.com') -> (11, 14)         # 不在起始位置匹配
    '''
    __logger.echo_msg(u"ready to execute[re_flexible]")
    try:
        return re.search(pattern, string, flags=re.X)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[re_flexible]")


def re_unicode(pattern, string):
    '''
                re_unicode(pattern, string) -> 匹配的对象 or None

                    功能：search 扫描整个字符串并返回第一个成功的匹配

                    参数:
                    pattern : 匹配的正则表达式.
                    string  : 要匹配的字符串.
                    flags   : 标志位，用于控制正则表达式的匹配方式
                             re.U 设置使用Unicode字符集
                    返回:
                            返回一个匹配的对象，否则返回None.
                    例子:
                    re_unicode('www', 'www.runoob.com').span() -> (0, 3)     # 在起始位置匹配
                    re_unicode('com', 'www.runoob.com') -> (11, 14)         # 不在起始位置匹配

                '''
    __logger.echo_msg(u"ready to execute[re_unicode]")
    try:
        return re.search(pattern, string, flags=re.U)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[re_unicode]")


def dict_updata_value(dict,key,value):
    '''
            dict_updata_value(dict,key,value) -> dict
                function：Updates the value of the specified key.
                parameter：
                  dict :Dictionary objects to be processed
                  key :Keys to be updated
                  value：Values to be updated
                return:
                    If this key is not in the dictionary, return False
                instance:
                dict_updata_value({'a': '123', 'b': 10000},'a','aaaaaaaa')
                dict_updata_value({'a': '123', 'b': 10000},'d','vvvvvvv')
    '''
    if key in dict:
        dict[key]=value
        #return dict
    else:
        return False


def dict_move(dict, key):
    '''
            dict_move(dict,key) -> str or int
                function：Delete the value corresponding to the given key in the dictionary.
                parameter：
                  dict :Dictionary objects to be processed
                  key :Key values to be deleted
                instance:
                dict_move({'a': '123', 'b': 10000},'a')

    '''
    dict.pop(key)

    #return dict


def dict_get(dict, key):
    '''
            dict_get(dict,key) -> str or int
                function：Returns the value of the specified key.
                parameter：
                  dict :Dictionary objects to be processed
                  key: The key to look up in the dictionary。
                return:
                    Returns the value of the specified key.
                instance:
                dict_get('a': '123', 'b': 10000},'a')         -> ‘123’

    '''
    return dict.get(key)


def dict_get_vals(dict):
    '''
            dict_get_vals(dict) -> list
                function：Returns a list containing all the values of the dictionary.
                parameter：
                  dict :Dictionary objects to be processed
                return:
                    Returns a list containing all the values of the dictionary.
                instance:
                dict_get_vals({'Sex': 'female', 'Age': 7, 'Name': 'Zara'})    -> ['female', 7, 'Zara']

    '''
    return list(dict.values())


def dict_key_in(dict,key):
    '''
            dict_key_in(dict,k) -> Ture or False
                function：Determine whether the key exists in the dictionary.
                parameter：
                  dict :Dictionary objects to be processed
                  key: The key to look up in the dictionary.
                return:
                    If the key returns Ture in dictionary dict, otherwise it returns False.
                instance:
                dict_key_in({'Sex': 'female', 'Age': 7, 'Name': 'Zara'},'Name')    -> Ture
                dict_key_in({'Sex': 'female', 'Age': 7, 'Name': 'Zara'},'qqq')     -> False
    '''
    return  (key in dict)


def dict_get_keys(dict):
    '''
            dict_get_keys(dict)  -> list
                function：Returns a list of all keys.
                parameter：
                  dict :Dictionary objects to be processed
                return:
                    Returns a list of all keys.
                instance:
                dict_get_keys({'Sex': 'female', 'Age': 7, 'Name': 'Zara'})     -> ['Sex', 'Age', 'Name']

    '''
    return list(dict.keys())


def dict_get_key(dict, key):
    '''
            dict_get_key(dict,key) -> str or int
                function：Returns the value of the specified key.
                parameter：
                  dict :Dictionary objects to be processed
                  key: The key to look up in the dictionary.
                return:
                   Returns the value of the specified key.
                instance:
                dict_get_key('a': '123', 'b': 10000},'a')         -> '123'

    '''
    return dict[key]


def dict_updata(a,b):
    '''
            dict_updata(a,b) -> dict
                function：Add the key/value pair of dictionary b to a.
                parameter：
                  a :Dictionary to be added
                  b: Added dictionary
                instance:
                dict_updata({'a': '123', 'b': 10000}, {'Sex': 'female', 'Age': 7, 'Name': 'Zara'})

    '''
    a.update(b)
    #return a


def add(a, b):
    '''
            add(a,b) -> int
                function：Add two numbers
                parameter：
                  a :number a
                  b: number b
                return:
                    Returns the sum of two numbers
                instance:
                add(1,2)  -> 3

    '''
    __logger.debug(u"ready to execute[add]")
    try:
        return a+b
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[add]")


def reduce(a, b):
    '''
            reduce(a,b) -> int
                function：a minus b
                parameter：
                  a :number a
                  b: number b
                return:
                    Returns the difference between two numbers
                instance:
                reduce(3,2)  -> 1

    '''
    __logger.debug(u"ready to execute[reduce]")
    try:
        return a-b
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[reduce]")


def multiply(a, b):
    '''
            multiply(a,b) -> int
                function：a multiply b
                parameter：
                  a :number a
                  b: number b
                return:
                    Returns the product of two numbers
                instance:
                multiply(3,2)  -> 6

    '''
    __logger.debug(u"ready to execute[multiply]")
    try:
        return a*b
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[multiply]")


def division(a, b):
    '''
            division(a,b) -> int
                function：a divided by b
                parameter：
                  a :number a
                  b: number b
                return:
                    Returns the quotient of two numbers
                instance:
                division(4,2)  -> 2

    '''
    __logger.debug(u"ready to execute[division]")
    try:
        return a/b
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[division]")


def ceil(x):
    '''
            ceil(x) -> int
                function：Take the smallest integer value greater than or equal to x
                parameter：
                  x :number x
                return:
                    Returns the smallest integer value greater than or equal to x
                instance:
                ceil(5)  -> 5
                ceil(5.68) -> 6
    '''
    __logger.debug(u"ready to execute[ceil]")
    try:
        return math.ceil(x)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[ceil]")


def exp(x):
    '''
            exp(x) -> num
                function：Return math.e, which is the power of 2.71828
                parameter：
                  x :number x
                return:
                    Returns math.e, which is the power of 2.71828
                instance:
                exp(1)  -> 2.718281828459045
                exp(2)  -> 7.38905609893065

    '''
    __logger.debug(u"ready to execute[exp]")
    try:
        return math.exp(x)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[exp]")


def fabs(x):
    '''
            fabs(x) -> num
                function：Return the absolute value of x
                parameter：
                  x :number x
                return:
                    Returns the absolute value of x
                instance:
                fabs(1)  -> 1
                fabs(-1) -> 1

    '''
    __logger.debug(u"ready to execute[fabs]")
    try:
        return math.fabs(x)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[fabs]")


def factorial(x):
    '''
            factorial(x) -> int
                function：Take the value of the factorial of x
                parameter：
                  x : int x
                return:
                    the value of the factorial of x
                instance:
                factorial(x=1)  -> 1
                factorial(x=2)  -> 2
                factorial(x=3)  -> 6
    '''
    __logger.debug(u"ready to execute[factorial]")
    try:
        return math.factorial(x)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[factorial]")


def floor(x):
    '''
            floor(x) -> int
                function：Take the largest integer value less than or equal to x, or return itself if x is an integer
                parameter：
                  x : int x
                return:
                    the largest integer value less than or equal to x, or return itself if x is an integer
                instance:
                floor(1)     -> 1
                floor(-1.5)  -> -2
                floor(5.8)   -> 5
    '''
    __logger.debug(u"ready to execute[floor]")
    try:
        return math.floor(x)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[floor]")


def fmod(x, y):
    '''
            fmod(x,y) -> float
                function：Get the remainder of x/y whose value is a floating point number
                parameter：
                  x : num x
                  y : num y
                return:
                    the remainder of x/y
                instance:
                fmod(1, 2)     -> 1.0
                fmod(1.5, 2.7) -> 1.5
                fmod(3, 3.7)   -> 3.0
    '''
    __logger.debug(u"ready to execute[fmod]")
    try:
        return math.fmod(x,y)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[fmod]")


def gcd(x, y):
    '''
            gcd(x, y) -> int
                function：Returns the greatest common divisor of x and y
                parameter：
                  x : int x
                  y : int y
                return:
                    the greatest common divisor of x and y
                instance:
                gcd(2, 8)     -> 2
                gcd(2, 9)     -> 1
                gcd(3, 17)    -> 1
    '''
    __logger.debug(u"ready to execute[gcd]")
    try:
        return math.gcd(x, y)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[gcd]")


def log(x, base=math.e):
    '''
            log(x, base=math.e) -> num
                function：Returns the natural logarithm of x. The default is e as the base. The base parameter is given. The logarithm of x is returned to the given base. The calculation is: log(x)/log(base)
                parameter：
                  x : num x
                  base : num
                return:
                    the natural logarithm of x. The default is e as the base
                instance:
                log(x=50)           ->  3.912023005428146
                log(x=50, base=100) ->  0.8494850021680093
    '''
    __logger.debug(u"ready to execute[log]")
    try:
        return math.log(x, base)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[log]")


def log10(x):
    '''
            log10(x) -> num
                function： Returns the base 10 logarithm of x
                parameter：
                  x : num x
                return:
                    the base 10 logarithm of x
                instance:
                log10(x=100) ->  2.0
                log10(x=180) ->  2.255272505103306
    '''
    __logger.debug(u"ready to execute[log10]")
    try:
        return math.log(x, 10)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[log10]")


def pow(x, y):
    '''
            pow(x, y) -> num
                function： Returns the y-th power of x, ie x**y
                parameter：
                  x : num x  Base
                  y : num y  power
                return:
                    the y-th power of x
                instance:
                pow(1.5,2.6) ->  2.8697051264080295
                pow(1.5,2)   ->  2.25
    '''

    __logger.debug(u"ready to execute[pow]")
    try:
        return math.pow(x, y)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[pow]")


def sqrt(x):
    '''
            sqrt(x) -> num
                function： Find the square root of x
                parameter：
                  x : num x
                return:
                    the square root of x
                instance:
                sqrt(4)     ->  2
                sqrt(4.5)   ->  2.1213203435596424
    '''
    __logger.debug(u"ready to execute[sqrt]")
    try:
        return math.sqrt(x)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[sqrt]")


def trunc(x):
    '''
            trunc(x) -> num
                function： Returns the integer part of x
                parameter：
                  x : num x
                return:
                    the integer part of x
                instance:
                trunc(2.1)   ->  2
                trunc(2.9)   ->  2
    '''

    __logger.debug(u"ready to execute[trunc]")
    try:
        return math.trunc(x)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[trunc]")


def math_round(x, n):
    '''
            math_round(x, n) -> num
                function： Returns the rounding value of the floating point number x, such as the value of n, which represents the number of digits rounded to the decimal point
                parameter：
                  x : num x
                  n : int n  Number of digits reserved
                return:
                    the rounding value of the floating point number x
                instance:
                round(3.12, 4)       ->  3.12
                round(3.123456, 4)   ->  3.1235
    '''

    __logger.debug(u"ready to execute[math_round]")
    try:
        return round(x, n)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[math_round]")


def random_randint(x, y):
    '''
            random_randint(x, y) -> int
                function： Used to generate an integer within a specified range. Where the parameter x is the lower limit, the parameter y is the upper limit, and the generated random number: x <= n <= y
                parameter：
                  x : int x  the lower limit
                  y : int y  the upper limit
                return:
                      an integer within a specified range
                instance:
                random_randint(1, 5)  ->  4
                random_randint(1, 7)  ->  5
    '''
    __logger.debug(u"ready to execute[random_randint]")
    try:
        return random.randint(x, y)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[random_randint]")


def random_choice(sequence):
    '''
            random_choice(sequence) -> Random element
                function： Random.choice gets a random element from the sequence. Its function prototype is: random.choice(sequence). The parameter sequence represents an ordered type.
                parameter：
                  sequence : Ordered type
                return:
                      Random element
                instance:
                random_choice(sequence=[1,2,3,4,5])  ->  3
                random_choice(sequence='我你他')     ->  他
                random_choice(sequence=[1,2,3,4,'a','b','c','d','e',{'x':111},{'y':222}]) ->  e
    '''

    __logger.debug(u"ready to execute[random_choice]")
    try:
        return random.choice(sequence)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[random_choice]")


def irange(stop, start=0, step=1):
    '''
            irange(stop, start=0, step=1) -> get a list
            function： get a list in a range
            parameter：
              start : a start number
              stop : a end number
              step : length of step
            return:
                  a list
            instance:
            irange(1, 9, 2)   -->  [1, 3, 5, 7]
            irange(1, 9)   -->  [1, 2, 3, 4, 5, 6, 7, 8, 9]
    '''

    __logger.debug(u"ready to execute[irange]")
    try:
        return range(start, stop, step)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[irange]")


