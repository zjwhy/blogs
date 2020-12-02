# -*- coding: utf-8 -*-
'''
Created on 2018。3.29
@author: Wu.Xin
主要用于win窗口的操作
'''

from ctypes import *
import datetime
import tempfile
import time
from ubpa import encrypt
from ubpa.iconstant import *
from ubpa.ierror import *
from ubpa.ilog import ILog, RpaServer
from ubpa.itools.http_sender import *
import ubpa.base_native_ait as nit
import getpass
import json
from urllib import request
import configparser
import chardet
import requests

__logger = ILog(__file__)

dll = windll.LoadLibrary("../Com.Isearch.Func.AutoIt/AutoItX3.dll")  # 调AutoItX3动态库

#dll = windll.LoadLibrary(r"D:\svn\isa\branches\ueba_5.0\makesetup\CdaSetupDate\plugin\Com.Isearch.Func.AutoIt\AutoItX\AutoItX3.dll")

'''
 激活某个窗口
win_title    :窗口标题
返回: True:成功

'''
def do_win_activate(win_title="", win_text="", waitfor=WAIT_FOR):
    __logger.debug('do_win_activate :[' + win_title + ']')
    try:
        starttime = time.time()
        dll.AU3_Opt("WinTitleMatchMode", 2)
        while True:
            
            rst = dll.AU3_WinActivate(win_title, win_text)
            
            if rst == 1:
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug('do_win_activate error:[' + win_title + ']')
                    raise WinNotFoundError('do_win_activate error:[' + win_title + ']')
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e


'''
 检查指定窗口是否存在且被激活
win_title    :窗口标题

返回: True:成功   False:失败

'''
def do_win_is_active(win_title="", win_text="", waitfor=1):
    __logger.debug('do_win_is_active:[' + win_title + ']')
    try:
        starttime = time.time()
        dll.AU3_Opt("WinTitleMatchMode", 2)
        while True:
            rst = dll.AU3_WinActive(win_title, win_text)
            if rst == 1:
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug('do win is not active :[' + win_title + ']')
                    return False
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e

'''
 最大化窗口
win_title    : 窗口标题
win_text     :窗口文本
waitfor      :超时
返回: True:成功   False:失败

'''
def do_win_maximize(win_title='', win_text=None, waitfor=WAIT_FOR):
    __logger.debug('do_win_maximize:[' + win_title + ']')

    try:
        starttime = time.time()
        dll.AU3_Opt("WinTitleMatchMode", 2)
        while True:
            rst = dll.AU3_WinSetState(win_title, "", 3)
            if rst == 1:
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug('window maximize error:[' + win_title + ']')
                    raise WinNotFoundError('window maximize error:[' + win_title + ']')
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e


'''
 最小化窗口
win_title    : 窗口标题
win_text     :窗口文本
waitfor      :超时
返回: True:成功   False:失败

'''
def do_win_minimize(win_title='', win_text=None, waitfor=WAIT_FOR):
    __logger.debug('do_win_minimize:[' + win_title + ']')
    try:
        starttime = time.time()
        dll.AU3_Opt("WinTitleMatchMode", 2)
        while True:
            rst = dll.AU3_WinSetState(win_title, "", 6)
            if rst == 1:
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug('do_win_minimize error:[' + win_title + ']')
                    raise WinNotFoundError('do_win_minimize error:[' + win_title + ']')
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e


'''
 关闭窗口
win_title    : 窗口标题
win_text     :窗口文本
waitfor      :超时
返回: True:成功   False:失败

'''
def do_win_close(win_title="", win_text=None, waitfor=WAIT_FOR):
    __logger.debug('do_win_close:[' + win_title + ']')
    try:
        starttime = time.time()
        dll.AU3_Opt("WinTitleMatchMode", 2)
        if win_title != "":
            while True:
                rst = dll.AU3_WinClose(win_title, "")
                if rst == 1:
                    return True
                else:
                    runtime = time.time() - starttime
                    if runtime >= waitfor:
                        __logger.debug('do_win_close error:[' + win_title + ']')
                        raise WinNotFoundError('do_win_close error:[' + win_title + ']')
                    time.sleep(TRY_INTERVAL)
        else:
            __logger.debug('win_title is null')
    except Exception as e:
        raise e


'''
 强行关闭指定窗口
win_title    : 窗口标题
win_text     :窗口文本
waitfor      :超时
返回: True:成功   False:失败

'''
def do_win_kill(win_title="", win_text=None, waitfor=WAIT_FOR):
    __logger.debug('ready to excute:[' + win_title + ']')
    try:
        starttime = time.time()
        dll.AU3_Opt("WinTitleMatchMode", 2)
        if win_title != "":
            while True:
                rst = dll.AU3_WinKill(win_title, "")
                if rst == 1:
                    return True
                else:
                    runtime = time.time() - starttime
                    if runtime >= waitfor:
                        __logger.debug('do_win_kill error:[' + win_title + ']')
                        raise WinNotFoundError('do_win_kill error:[' + win_title + ']')
                    time.sleep(TRY_INTERVAL)
        else:
            __logger.debug('win_title is null')
    except Exception as e:
        raise e


'''
组装au3的代码
'''
def pack_au3_data():
    pre_msg = "#include <MsgBoxConstants.au3>" \
              + '\n' + "Local $str = ''" \
              + '\n' + "Local $aList = WinList()" \
              + '\n' + "For $i = 1 To $aList[0][0]" \
              + '\n' + "  If $aList[$i][0] <> '' And BitAND(WinGetState($aList[$i][1]), 2) Then" \
              + '\n' + "      $str = $str &','& $aList[$i][0]" \
              + '\n' + "  EndIf" \
              + '\n' + "Next" \
              + '\n' + 'ConsoleWrite($str)'
    return pre_msg


'''
遍历窗口标题
'''
def do_win_list():
    __logger.debug('win_title_list')
    try:
            msg = pack_au3_data()  ##组装生成au3所需的数据
            tmp_au3_file_path = nit.gen_au3_file(msg)  # 生成XXX.au3文件并返回路径
            status, error_string, stdout_string = nit.run_autoit(tmp_au3_file_path)
            nit.cleanup(tmp_au3_file_path)
            plist = str(get_win_list_string(stdout_string))
            return plist
    except Exception as e:
        raise e

def get_win_list_string(msg_string):
    return u' '.join(
        line for line in msg_string.decode('utf-8').splitlines()
    ).strip()

def do_process_close(pcocess=None):
    '''
    关闭进程
    '''
    __logger.debug('Ready to close the application')
    try:
        while True:
            p_exist = dll.AU3_ProcessExists(pcocess)
            if p_exist == 0 :
                break
            elif p_exist != 0 :
                rst = dll.AU3_ProcessClose(pcocess)
                if rst != 1:
                    break
    except Exception as e:
        raise e


def unlock_screen(uname,upass,try_times=3, esc_wait_time=2000,next_wait_time=2000):
    ldll = windll.LoadLibrary("../Com.Isearch.Driver.WinIO/RpaAutoLogin.dll")
    upass = encrypt.decrypt(upass)
#     ldll = windll.LoadLibrary(r"D:\svn\isa\branches\ueba_5.0\makesetup\CdaSetupDate\plugin\Com.Isearch.Driver.WinIO\RpaAutoLogin.dll")
    result = ldll.do_autologin(uname,upass,try_times,esc_wait_time,next_wait_time)
    return result


def unlock_screen_remote(uname='',domain='',upass='',addr='',port=3389,try_interval=2, waitfor=60):
    try:
        screen_dll = windll.LoadLibrary("../Com.Isearch.Func.ScreenLock/ScreenLockCheck.dll")
        char_name = screen_dll.GetCurrentUsername()                 # 调用dll 获取 uname
        uname = string_at(char_name, -1).decode('utf-8')
        screen_dll.FreePointer(char_name)

        char_domain = screen_dll.GetCurrentDomain()
        domain = string_at(char_domain, -1).decode('utf-8')       # 调用dll 获取 domain
        screen_dll.FreePointer(char_domain)

        rpasever = RpaServer()
        agentUUID = rpasever.AgentUUID
        mainServer = rpasever.MainServer
        webServicePort = rpasever.WebServicePort

        starttime = time.time()
        has_send_http_flag = False
        while True:
            screen_status = is_screen_locked()
            if screen_status == 0:
                __logger.debug('The screen is now unlocked')
                return True
            else:
                if has_send_http_flag == False:   # 未成功发送过http请求
                    upass = encrypt.decrypt(upass)
                    data = {"msg_type":"rpa", "a": "conn_desk", "agent_no": agentUUID, "user_name": uname, "user_pass": upass,
                                 "addr": addr, "port": str(port), "scale": "100", "resolution": "widthXheight",
                                 "timeout": "60","user_domain":domain}
                    http_url = 'http://' + str(mainServer) + ":" + str(webServicePort)+'/wservice.action'
                    whole_request_url = http_url + '?jsonStr=' + str(data)
                    res = requests.get(whole_request_url)
                    dict = json.loads(str(res.text))
                    status = dict['status']
                    if status == '0':
                        has_send_http_flag = True
                        __logger.debug('Has sent a screen request')
                else:    # 成功发送过http请求
                    runtime = time.time() - starttime
                    if runtime >= waitfor:
                        __logger.debug('Operation timeout')
                        raise Exception
                time.sleep(try_interval)
    except Exception as e:
        raise e


def is_screen_locked():
    '''
    调用dll 判断是否为锁屏状态
    :return:   0  (int) 未锁屏状态
               1  (int) 锁屏状态
    '''
    screen_dll = windll.LoadLibrary("../Com.Isearch.Func.ScreenLock/ScreenLockCheck.dll")
    result = screen_dll.IsScreenLock()
    return result

def oper_lock(tip_show=1,timeout=0):
    '''
    鼠标键盘操作锁定
      NONE                     tip_show=0
      LEFT_TOP                 tip_show=1
      RIGHT_TOP                tip_show=2
      LEFT_BOTTOM              tip_show=3
      RIGHT_BOTTOM             tip_show=4

    '''
    oper_lock_dll = windll.LoadLibrary("../Com.Isearch.DesktopOperLock/DesktopOperLock.dll")
    oper_lock_dll.Lock(tip_show,timeout)



# do_win_close("记事本")