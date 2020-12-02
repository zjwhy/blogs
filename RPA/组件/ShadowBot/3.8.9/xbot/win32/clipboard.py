'''
剪切板模块
'''

import os
from .._core import uidriver


def set_text(value):
    '''
    设置剪切板文本内容
    * @param value, 要设置到剪切板中的文本
    '''

    _invoke("SetText", {"value":value})

def get_text()->str:
    '''
    获取剪切板文本内容
    * @return `str`, 返回当前剪切板中的文本内容
    '''

    return _invoke("GetText")

def clear():
    '''
    清空剪切板内容
    '''

    _invoke("Clear")

def set_file(file_paths):
    '''
    将文件添加到剪切板
    * @parame file_paths,文件绝对路径列表, 如['D:\\123.txt', 'D:\\234.xml']
    '''
    if file_paths is None or len(file_paths) == 0:
        raise ValueError('文件列表不能为空')

    for file in file_paths:
        if not os.path.exists(file):
            raise ValueError(f'{file}不存在')

    _invoke("SetFile", {'filePaths':file_paths})

def get_file_path()-> list:
    '''
    获取剪切板中文件(夹)路径列表
    * @return `str`, 返回当前剪切板中文件(夹)路径列表
    '''

    return _invoke("GetFilePaths")


def _invoke(action, args=None):
    return uidriver.execute(f'Clipboard.{action}', args)