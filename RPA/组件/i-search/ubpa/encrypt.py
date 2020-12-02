# -*- coding:utf-8 -*-
from ctypes import cdll, string_at
dll = cdll.LoadLibrary("../../bin/EncryptUtil.dll")

def encrypt(str):
    '''
    加密算法
    '''
    text = ''
    try:
        text = string_at(dll.Encrypt(str), -1).decode('utf-8')
    except Exception as e:
        raise e
    finally:
        return text


def decrypt(str):
    '''
    解密算法
    '''
    text = ''
    try:
        
        text = string_at(dll.Decrypt(str), -1).decode('utf-8')
    except Exception as e:
        raise e
    finally:
        return text







