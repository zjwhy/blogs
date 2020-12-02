# -*- coding: utf-8 -*-
from ubpa.ilog import ILog
from ctypes import *
from ctypes.wintypes import *


__logger = ILog(__file__)

dll = windll.LoadLibrary("../Com.Isearch.Func.AutoIt/AutoItX3.dll")
#dll = windll.LoadLibrary("D:/svn/isa/branches/ueba_5.0/makesetup/CdaSetupDate/plugin/Com.Isearch.Func.AutoIt/AutoItX/AutoItX3.dll")

def get_clipboard(mode=''):
    __logger.debug('Get from clipboard')
    try:
        buf_size = 2048
        clip = ctypes.create_unicode_buffer(buf_size)
        dll.AU3_ClipGet(clip, ctypes.c_int(buf_size))
        return clip.value.rstrip()
    except Exception as e:
        raise e
    finally:
        __logger.debug('Get from clipboard:['+str(clip.value.rstrip())+']')

def set_clipboard(text=''):
    __logger.debug('copy to clipboard:[' + str(text) + ']')
    try:
        return dll.AU3_ClipPut(LPCWSTR(str(text)))
    except Exception as e:
        raise e

