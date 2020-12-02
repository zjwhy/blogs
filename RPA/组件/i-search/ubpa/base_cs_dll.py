# -*- coding: utf-8 -*-
from ctypes import *
import json
from ctypes.wintypes import *
import win32com.client
import ubpa.base_img as img
from ubpa.base_native_ait import *


dll = windll.LoadLibrary("../Com.Isearch.Func.AutoIt/AutoItX3.dll")  # 调AutoItX3动态库
DEFAULT = -2147483647

def dllRun(param):
    dicResult = {}
    try:
        dic = getParam(param)
        param3 = dic["param3"]

        runPid = dll.AU3_Run(param3, "", 1)
        dicResult["run"] = runPid
        return dicResult
    except Exception as e:
        raise e

def dllMouseClick(param):
    dicResult = {}
    try:
        dic = getParam(param)
        param5 = dic["param5"]
        param6 = dic["param6"]
        dll.AU3_Opt("MouseCoordMode", 0)
        mouseClick = dll.AU3_MouseClick("left", int(param5[2:]), int(param6[2:]), 1, -1) #注意转换成int类型
        dicResult["mouseClick"] = mouseClick
        return dicResult
    except Exception as e:
        raise e

def dllControlSend(param):
    dicResult = {}
    try:
        dic = getParam(param)
        param1 = dic["param1"]
        param2 = dic["param2"]
        param3 = dic["param3"]
        controlSend = dll.AU3_ControlSend(param1, "", param2, param3, 0);
        dicResult["controlSend"] = controlSend
        return dicResult
    except Exception as e:
        raise e

def dllSend(param):
    dicResult = {}
    try:
        dic = getParam(param)
        param3 = dic["param3"]
        send = dll.AU3_Send(param3, 0);
        dicResult["send"] = send
        return dicResult
    except Exception as e:
        raise e

def dllonClick(param):
    dicResult = {}
    try:
        dic = getParam(param)
        param1 = dic["param1"]  # 标题
        param2 = dic["param2"]  # 主元素
        print(param2)
        onClick = dll.AU3_ControlClick(param1, "", param2, "left", 1, DEFAULT, DEFAULT)  # 有可能返回0，返回1，或者报错
        dicResult["onClick"] = onClick
        return dicResult
    except Exception as e:
        raise e



def dllsetText(param):
    dicResult = {}
    try:
        dic = getParam(param)
        param1 = dic["param1"]  # 标题
        param2 = dic["param2"]  # 主元素
        param3 = dic["param3"]  # 要设置的值
        setText = dll.AU3_ControlSetText(param1, "", param2, param3)  # 有可能返回0，返回1，或者报错
        dicResult["setText"] = setText
        return dicResult
    except Exception as e:
        raise e

def dllwinWaiteActive(param):
    dicResult = {}
    try:
        dic = getParam(param)
        param1 = dic["param1"]  # 标题
        winWaitActive = dll.AU3_WinWaitActive(param1, "", 20)  # 有可能返回0，返回1，或者报错
        dicResult["winWaitActive"] = winWaitActive
        return dicResult
    except Exception as e:
        raise e

def dllgetText(param):
    dicResult = {}
    try:
        dic = getParam(param)
        param1 = dic["param1"]  # 标题
        param2 = dic["param2"]  # 主元素
        buf_size = 256
        ctrl_text = ctypes.create_unicode_buffer(buf_size)
        dll.AU3_ControlGetText(param1, "", param2, ctrl_text, buf_size)
        getText = ctrl_text.value.rstrip()
        dicResult["getText"] = getText
        return dicResult
    except Exception as e:
        raise e

def dllWinActivate(win_title="",win_text=None):
    dicResult = {}
    try:
        win_activate = dll.AU3_WinActivate(win_title,"") # 返回1:窗口已激活 0:有可能参数错误导致窗口未激活
        dicResult["win_activate"] = win_activate
        return dicResult
    except Exception as e:
        raise e

def dllWinClose(win_title="",win_text=None):
    dicResult = {}
    try:
        win_close = dll.AU3_WinClose(win_title,"") #返回1:窗口已关闭 0:有可能是参数错误导致窗口未关闭
        dicResult["win_close"] = win_close         # 窗口关闭并不等于窗口已退出 进程依然在
        return dicResult
    except Exception as e:
        raise e

def dllWinKill(win_title="",win_text=None):
    dicResult = {}
    try:
        win_kill = dll.AU3_WinKill(win_title,"")
        dicResult["win_kill"] = win_kill
        return dicResult
    except Exception as e:
        raise e

def dllWinMaxmize(win_title="",win_text=None):
    dicResult = {}
    try:
        win_maxmize = dll.AU3_WinSetState(win_title,"",3) #返回1:窗口最大化 0:有可能是参数错误导致窗口未最大化
        dicResult["win_maxmize"] = win_maxmize
        return dicResult
    except Exception as e:
        raise e

def dllWinMinmize(win_title="",win_text=None):
    dicResult = {}
    try:
        win_minmize = dll.AU3_WinSetState(win_title,"",6) #返回1:窗口最小化 0:有可能是参数错误导致窗口未最小化
        dicResult["win_minmize"] = win_minmize
        return dicResult
    except Exception as e:
        raise e

def dllControlCommand(win_title,win_text,target,select_sring):
    dicResult = {}
    try:
        control_command = dll.AU3_ControlCommand(win_title, win_text, target,"SelectString",select_sring,"",256)
        dicResult["control_command"] = control_command
        return dicResult
    except Exception as e:
        raise e

def getWinList():
    dicResult = {}
    try:
        msg = pack_au3_data() ##组装生成au3所需的数据
        tmp_au3_file_path = img.gen_au3_file(msg)  # 生成XXX.au3文件并返回路径
        status, error_string, stdout_string = run_autoit(tmp_au3_file_path)
        dicResult["winlist"] = string_at(stdout_string, -1).decode('utf-8')

        img.__cleanup(tmp_au3_file_path)

        return dicResult
    except Exception as e:
        raise e




# param1:标题
# param2:定位元素
# param3:setText的时候需要添加的内容   send 方法  模拟键盘键
# param5: X轴坐标
# param6: Y轴坐标

def getParam(param):
    dic = {}
    param2 = ""
    param5 = ""
    param6 = ""
    paramJason = json.loads(param)
    target = paramJason.get("target")
    input = paramJason.get("input")
    if target != None:
        target = json.loads(param)["target"]

        WinTitle = target.get('WinTitle', "")  # 标题  param1

        WinClass = target.get('WinClass', "")  # 窗口class
        if WinClass != "":
            param2 = param2 + "WINCLASS:" + str(WinClass) + ";"

        WinPosition = target.get('WinPosition', "")  # 窗口位置
        if WinPosition != "":
            param2 = param2 + str(WinPosition) + ";"

        WinSize = target.get('WinSize', "")  # 窗口大小
        if WinSize != "":
            param2 = param2 + "WINSIZE:" + str(WinSize) + ";"

        WinStyle = target.get('WinStyle', "")  # 窗口样式
        if WinStyle != "":
            param2 = param2 + "WINSTYLE:" + str(WinStyle) + ";"

        WinExStyle = target.get('WinExStyle', "")  # 窗口外部样式
        if WinExStyle != "":
            param2 = param2 + "WINEXSTYLE:" + str(WinExStyle) + ";"

        WinHandle = target.get('WinHandle', "")  # 窗口句柄
        if WinHandle != "":
            param2 = param2 + "WINHANDLE:" + str(WinHandle) + ";"

        ConClass = target.get('ConClass', "")  # 组件class
        if ConClass != "":
            param2 = param2 + str(ConClass) + ";"

        ConInstance = target.get('ConInstance', "")  # instance
        if ConInstance != "":
            param2 = param2 + "INSTANCE:" + ConInstance + ";"

        ConClassName = target.get('ConClassName', "")  # 组件class名称
        if ConClassName != "":
            param2 = param2 + "CLASS:" + ConClassName + ";"

        ConName = target.get('ConName', "")  # 组件名称
        if ConName != "":
            param2 = param2 + "NAME:" + str(ConName) + ";"

        ConAdvanced = target.get('ConAdvanced', "")  # 高级选项
        if ConAdvanced != "":
            param2 = param2 + ConAdvanced + ";"

        ConID = target.get('ConID', "")  # 组件ID
        if ConID != "":
            param2 = param2 + "ID:" + str(ConID) + ";"

        ConText = target.get('ConText', "")  # 组件text文本
        if ConText != "":
            param2 = param2 + "TEXT:" + ConText + ";"

        ConPosition = target.get('ConPosition', "")  # 组件位置
        if ConPosition != "":
            postion = ConPosition.split(',')
            if ("X") in postion[0]:
                param5 = postion[0]
                param6 = postion[1]
            if ("X") in postion[1]:
                param5 = postion[1]
                param6 = postion[0]

        ConSize = target.get('ConSize', "")  # 组件大小
        if ConSize != "":
            param2 = param2 + "SIZE:" + ConSize + ";"

        ConControlClick = target.get('ConControlClick', "")
        if ConControlClick != "":
            param2 = param2 + ConControlClick + ";"

        ConStyle = target.get('ConStyle', "")  # 组件样式
        if ConStyle != "":
            param2 = param2 + "STYLE:" + ConStyle + ";"

        ConExStyle = target.get('ConExStyle', "")  # 组件外部样式
        if ConExStyle != "":
            param2 = param2 + "EXSTYLE:" + ConExStyle + ";"

        ConHandle = target.get('ConHandle', "")  # 组件句柄
        if ConHandle != "":
            param2 = param2 + "HANDLE:" + ConHandle + ";"

        dic["param1"] = WinTitle  # 标题
        dic["param2"] = "[" + param2[:-1] + "]"  # 定位参数
        dic["param5"] = param5
        dic["param6"] = param6

    if input != None:
        input = json.loads(param)["input"]
        text = input.get('text', "")
        dic["param3"] = str(text)  # setText中的set参数

    return dic

def pack_au3_data():

    pre_msg =  "#include <MsgBoxConstants.au3>" \
            + '\n' + "Local $str = ''" \
            + '\n' + "Local $aList = WinList()" \
            + '\n' + "For $i = 1 To $aList[0][0]" \
            + '\n' + "  If $aList[$i][0] <> '' And BitAND(WinGetState($aList[$i][1]), 2) Then" \
            + '\n' + "      $str = $str &','& $aList[$i][0]" \
            + '\n' + "  EndIf" \
            + '\n' + "Next" \
            + '\n' + 'ConsoleWrite($str)'
    return pre_msg


