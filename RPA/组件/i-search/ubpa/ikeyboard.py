# -*- coding: utf-8 -*-
'''
Created on 2018。3.29

@author: Wu.Xin

主要用于键盘类的操作
'''

from ctypes import * 
from ubpa.ierror import *
from ubpa.iconstant import *
from ubpa.ilog import ILog 
import ubpa.iwin as iwin
import ubpa.encrypt as encrypt
import time
__logger = ILog(__file__)

dll = windll.LoadLibrary("../Com.Isearch.Func.AutoIt/AutoItX3.dll")  # 调AutoItX3动态库

str_dll = windll.LoadLibrary("../Com.Isearch.Driver.WinIO/RpaClientWinio.dll")

'''
 发送键盘事件
win_title   :窗口标题
'''
def key_send_cs(win_title=None,text=None,waitfor=WAIT_FOR):
    __logger.debug('keyboard send key:[win:'+str(win_title)+']'+str(text))
    try:        
        ''''如果指定窗口'''
        if(win_title != None ):
            ''''如果窗口不活跃状态'''
            if not iwin.do_win_is_active(win_title) : 
                iwin.do_win_activate(win_title=win_title, waitfor = waitfor)
        text = encrypt.decrypt(text)
        dll.AU3_Send(str(text), 0)
    except Exception as e:
        raise e


'''
 热键发送
win_title   :窗口标题
'''


def hotkey_send_cs(win_title=None, text=None, waitfor=WAIT_FOR):
    __logger.debug('hotkey send key:[win:' + str(win_title) + ']' + str(text))
    try:
        ''''如果指定窗口'''
        if (win_title != None):
            ''''如果窗口不活跃状态'''
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)

        dll.AU3_Send(str(text), 0)
    except Exception as e:
        raise e

def control_send_cs(win_title=None,text=None,waitfor=WAIT_FOR):
    '''
    :param win_title: 窗口标题
    :param text: 设置参数
    :param waitfor:  等待时间
    :return:
    '''
    __logger.debug('str control send:[win:' + str(win_title) + ']' + str(text))
    starttime = time.time()
    try:
        while True:

            ''''如果指定窗口'''
            if (win_title != None):
                ''''如果窗口不活跃状态'''
                if not iwin.do_win_is_active(win_title):
                    iwin.do_win_activate(win_title=win_title, waitfor=waitfor)

            text = encrypt.decrypt(text)
            result = str_dll.setElementValue(text)
            err = string_at(str_dll.getLastError(), -1).decode('utf-8')
            if err == "":
                return result
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'timeout ' + err)
                    raise ExcuteError('control send error:[' + win_title + ']')
                __logger.debug(r'try fail ,wait next' + err)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e