from xbot._core import robot
import os, ctypes
import threading
import time
import argparse
import math
from collections import namedtuple

cmd_parser = argparse.ArgumentParser(allow_abbrev=True)
cmd_parser.add_argument('--disable-block-progress', type=bool, required=False)
cmd_args, _ = cmd_parser.parse_known_args()
disable_block_progress = cmd_args.disable_block_progress
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def excel_column_name_to_index(column_name):
    """Excel列名称转列索引，从1开始"""
    index = 0
    for li, ln in enumerate(column_name[::-1]):
        if li == 0:
            index = index + ord(ln)-64
        else:
            index = index + math.pow(26, li) * (ord(ln)-64)
    return int(index)


def excel_column_index_to_name(col_index):
    """Excel列索引转列名称，从1开始"""
    result = []
    while col_index:
        col_index, rem = divmod(col_index-1, 26)
        result[:0] = LETTERS[rem]
    return ''.join(result)


def parsesudoku_from_args(args, key, default='middleCenter') -> str:
    return args.get(key, default)


def parseint_from_args(args, key, default=0):
    value = args.get(key, default)
    if isinstance(value, int):
        return value
    elif isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            raise ValueError(f'参数{key}类型错误, 必须为整数类型')
    else:
        raise ValueError(f'参数{key}类型错误, 必须为整数类型')


def parsefloat_from_args(args, key, default=0):
    value = args.get(key, default)
    if isinstance(value, (int, float)):
        return value
    elif isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            raise ValueError(f'参数{key}类型错误, 必须为数字类型')
    else:
        raise ValueError(f'参数{key}类型错误, 必须为数字类型')


def visual_action(func):
    def wrapper(**kwargs):
        inputs = {}
        try:
            if kwargs is not None:

                # 通知Block进度
                if not disable_block_progress:
                    # ("main", 4, "打开网页")
                    block_info = kwargs.pop('_block', None)
                    if block_info is not None:
                        _progress.report(block_info)

                for key, value in kwargs.items():
                    if _isalambda(value):
                        inputs[key] = value()  # calc lambda
                    else:
                        inputs[key] = value
            return func(**inputs)
        except Exception as e:
            if inputs.get('_ignore_exception', 'False') == 'True':
                print(f'{e}')
            else:
                raise e
        finally:
            pass
    return wrapper

# python dict 转 python object
# object通过.来访问属性， dict通过['']来访问key
def dict_to_object(typename, d):
    return namedtuple(typename, d.keys())(*d.values())



def _isalambda(v):
    return callable(v) and v.__name__ == '<lambda>'

def _expand_path(path):
    '''
    功能：将path中的环境变量替换成实际路径
    '''
    ret_path = ctypes.create_unicode_buffer(1024)
    ctypes.windll.Kernel32.ExpandEnvironmentStringsW(path, ret_path, 1024)
    return ret_path.value

class _Progress(object):
    """ 实现Flow进度通知功能
        通知Flow改变Block状态，为了防止刷新过于频繁，这里通过timer降低频率
    """

    def __init__(self):
        self._block_info = None
        self._thread = threading.Thread(target=self._monitor, daemon=True)
        self._thread.start()

    def report(self, block_info):
        self._block_info = block_info

    def _monitor(self):
        while True:
            block_info = self._block_info
            self._block_info = None
            if block_info is not None:
                robot.execute(f'Progress.HitBlock', {
                              'flowName': block_info[0], 'line': block_info[1], 'blockTitle': block_info[2]})
            time.sleep(0.5)


_progress = _Progress()
