from .app import logging
from . import web, win32, ai, ado, app, selector, primitives, errors, pdf, excel, mobile, xzip

import io as _io
import builtins as _builtins
import time as _time


def print(*values, sep=' ', end='', file=None, flush=False):
    """
    打印日志
    * @param values, 需要打印的一个或多个对象
    * @param sep, 多个打印对象之间的分隔符，默认是空格
    * @param end, 打印内容后缀，默认空字符串
    * @param file, 请勿使用此参数，或者考虑使用`builtins.print`
    * @param flush, 请勿使用此参数，或者考虑使用`builtins.print`
    """
    if file is None:
        value = None
        with _io.StringIO() as fs:
            _builtins.print(*values, sep=sep, end=end, file=fs, flush=True)
            value = fs.getvalue()
        logging.info(value)
    else:
        _builtins.print(*values, sep=sep, end=end, file=file, flush=flush)

def sleep(secs: float):
    """
    暂停指定时间
    * @param secs, 暂停时长(单位:秒)
    """
    _time.sleep(secs)
