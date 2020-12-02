# -*- coding: utf-8 -*-
import ubpa.base_cs_dll
import datetime
from ctypes import *
from ubpa.ilog import ILog
from ubpa.iresult import IResult
import traceback
import time

print("begin")
__try_times = 2

__logger = ILog(__file__)

#运行程序
def run_cs(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[run_cs]")

    iresult = IResult()  # new一个返回结果的新对象
    iresult.status = 0  # status初始赋值   status =0 成功  1 表示失败

    try:
        dicResult = ubpa.base_cs_dll.dllRun(param)
        stringRst = dicResult["run"]
        if stringRst == 0:  # 返回pid  为0表示没有运行成功

            for le in range(0, __try_times):

                __logger.info(str((le + 1)) + "times," + "Afferent parameter:" + param)

                dicResult = ubpa.base_cs_dll.dllRun(param)
                stringRst = dicResult["run"]
                if stringRst != 0:
                    __logger.info(str((le + 1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst == 0:
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = dicResult["run"]
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[run_cs]")


# #左键1次
def do_click_cs(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[do_click_cs]")

    iresult = IResult()
    iresult.status = 0

    try:
        dicResult = ubpa.base_cs_dll.dllonClick(param)
        stringRst = dicResult["onClick"]
        if stringRst != 1:

            for le in range(0, __try_times):

                __logger.info(str((le + 1)) + "times," + "Afferent parameter:" + param)

                dicResult = ubpa.base_cs_dll.dllonClick(param)
                stringRst = dicResult["onClick"]
                if stringRst == 1:
                    __logger.info(str((le + 1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != 1:
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = dicResult["onClick"]
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[do_click_cs]")


# #设置input框值
def control_set_text_cs(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[control_set_text_cs]")

    iresult = IResult()
    iresult.status = 0

    try:
        dicResult = ubpa.base_cs_dll.dllsetText(param)
        stringRst = dicResult["setText"]
        if stringRst != 1:  #

            for le in range(0, __try_times):

                __logger.info(str((le + 1)) + "times," + "Afferent parameter:" + param)

                dicResult = ubpa.base_cs_dll.dllsetText(param)
                stringRst = dicResult["setText"]
                if stringRst == 1:
                    __logger.info(str((le + 1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != 1:
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = dicResult["setText"]
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[control_set_text_cs]")


# #等待窗口激活
def win_wait_active_cs(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[win_wait_active_cs]")

    iresult = IResult()
    iresult.status = 0

    try:
        dicResult = ubpa.base_cs_dll.dllwinWaiteActive(param)
        stringRst = dicResult["winWaitActive"]
        if stringRst != 1:

            for le in range(0, __try_times):

                __logger.info(str((le + 1)) + "times," + "Afferent parameter:" + param)

                dicResult = ubpa.base_cs_dll.dllwinWaiteActive(param)
                stringRst = dicResult["winWaitActive"]
                if stringRst == 1:
                    __logger.info(str((le + 1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != 1:
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = dicResult["winWaitActive"]
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[win_wait_active_cs]")


# #获取input框值
def control_get_text_cs(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[control_get_text_cs]")

    iresult = IResult()
    iresult.status = 0

    try:
        dicResult = ubpa.base_cs_dll.dllgetText(param)
        stringRst = dicResult["getText"]
        if str(stringRst) == "":  # 表示没取到

            for le in range(0, __try_times):

                __logger.info(str((le + 1)) + "times," + "Afferent parameter:" + param)

                dicResult = ubpa.base_cs_dll.dllgetText(param)
                stringRst = dicResult["getText"]
                if stringRst != "":
                    __logger.info(str((le + 1)) + "times,try success")
                    break

                time.sleep(1)

        if str(stringRst) == "":
            __logger.info(u"Interface returns error information:" + str(stringRst))

        iresult.obj = dicResult["getText"]
        iresult.echo_result()
        return iresult
    except Exception as e:
        print(e)
    finally:
        __logger.echo_msg(u"end execute[control_get_text_cs]")



# #鼠标根据X,Y位置点击 相对于控件位置
def mouse_click_cs(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[mouse_click_cs]")

    iresult = IResult()
    iresult.status = 0

    try:
        dicResult = ubpa.base_cs_dll.dllMouseClick(param)
        stringRst = dicResult["mouseClick"]
        if stringRst != 1:

            for le in range(0, __try_times):

                __logger.info(str((le + 1)) + "times," + "Afferent parameter:" + param)

                dicResult = ubpa.base_cs_dll.dllMouseClick(param)
                stringRst = dicResult["mouseClick"]
                if stringRst == 1:
                    __logger.info(str((le + 1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != 1:
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = dicResult["mouseClick"]
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[mouse_click_cs]")


# #获取input框值
def control_send_cs(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[control_send_cs]")

    iresult = IResult()
    iresult.status = 0

    try:
        dicResult = ubpa.base_cs_dll.dllControlSend(param)
        stringRst = dicResult["controlSend"]
        if stringRst != 1:

            for le in range(0, __try_times):

                __logger.info(str((le + 1)) + "times," + "Afferent parameter:" + param)

                dicResult = ubpa.base_cs_dll.dllControlSend(param)
                stringRst = dicResult["controlSend"]
                if stringRst == 1:
                    __logger.info(str((le + 1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != 1:
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = dicResult["controlSend"]
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[control_send_cs]")


# #发送按钮
def key_send_cs(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[key_send_cs]")

    iresult = IResult()
    iresult.status = 0

    try:
        dicResult = ubpa.base_cs_dll.dllSend(param)
        stringRst = dicResult["send"]
        if stringRst != 1:

            for le in range(0, __try_times):

                __logger.info(str((le + 1)) + "times," + "Afferent parameter:" + param)

                dicResult = ubpa.base_cs_dll.dllSend(param)
                stringRst = dicResult["send"]
                if stringRst == 1:
                    __logger.info(str((le + 1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != 1:
            __logger.info(u"Interface returns error information:" + str(stringRst))

        iresult.obj = dicResult["send"]
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[key_send_cs]")

# #发送按钮
def hotkey_send_cs(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[hotkey_send_cs]")

    iresult = IResult()
    iresult.status = 0

    try:
        dicResult = ubpa.base_cs_dll.dllSend(param)
        stringRst = dicResult["send"]
        if stringRst != 1:

            for le in range(0, __try_times):

                __logger.info(str((le + 1)) + "times," + "Afferent parameter:" + param)

                dicResult = ubpa.base_cs_dll.dllSend(param)
                stringRst = dicResult["send"]
                if stringRst == 1:
                    __logger.info(str((le + 1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != 1:
            __logger.info(u"Interface returns error information:" + str(stringRst))

        iresult.obj = dicResult["send"]
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[hotkey_send_cs]")


# #激活窗口
def do_win_activate(win_title="",win_text=None):
    __logger.info(u"Afferent parameter:win_title:" + str(win_title))
    __logger.echo_msg(u"Ready to execute[win_activate_cs]")

    iresult = IResult()
    iresult.status = 0

    try:
        dicResult = ubpa.base_cs_dll.dllWinActivate(win_title,win_text)
        stringRst = dicResult["win_activate"]
        if stringRst != 1:

            for le in range(0, __try_times):

                __logger.info(str((le + 1)) + "times," + "Afferent parameter:win_title:" + str(win_title))

                dicResult = ubpa.base_cs_dll.dllWinActivate(win_title,win_text)
                stringRst = dicResult["win_activate"]
                if stringRst == 1:
                    __logger.info(str((le + 1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != 1:
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = dicResult["win_activate"]
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[win_activate_cs]")


# #关闭窗口
def do_win_close(win_title="",win_text=None):
    __logger.info(u"Afferent parameter:win_title:" + str(win_title))
    __logger.echo_msg(u"Ready to execute[win_close_cs]")

    iresult = IResult()
    iresult.status = 0

    try:
        dicResult = ubpa.base_cs_dll.dllWinClose(win_title,win_text)
        stringRst = dicResult["win_close"]
        if stringRst != 1:

            for le in range(0, __try_times):

                __logger.info(str((le + 1)) + "times," + "Afferent parameter:win_title:" + str(win_title))

                dicResult = ubpa.base_cs_dll.dllWinClose(win_title,win_text)
                stringRst = dicResult["win_close"]
                if stringRst == 1:
                    __logger.info(str((le + 1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != 1:
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = dicResult["win_close"]
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[win_close_cs]")


# #强制关闭关闭窗口
def do_win_kill(win_title="",win_text=None):
    __logger.info(u"Afferent parameter:win_title:" + str(win_title))
    __logger.echo_msg(u"Ready to execute[win_kill_cs]")

    iresult = IResult()
    iresult.status = 0

    try:
        dicResult = ubpa.base_cs_dll.dllWinKill(win_title,win_text)
        stringRst = dicResult["win_kill"]
        if stringRst != 1:

            for le in range(0, __try_times):

                __logger.info(str((le + 1)) + "times," + "Afferent parameter:win_title:" + str(win_title))

                dicResult = ubpa.base_cs_dll.dllWinKill(win_title,win_text)
                stringRst = dicResult["win_kill"]
                if stringRst == 1:
                    __logger.info(str((le + 1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != 1:
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = dicResult["win_kill"]
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[win_kill_cs]")


# #窗口最大化
def do_win_maximize(win_title="",win_text=None):
    __logger.info(u"Afferent parameter:win_title:" + str(win_title))
    __logger.echo_msg(u"Ready to execute[win_maxmize_cs]")

    iresult = IResult()
    iresult.status = 0

    try:
        dicResult = ubpa.base_cs_dll.dllWinMaxmize(win_title,win_text)
        stringRst = dicResult["win_maxmize"]
        if stringRst != 1:

            for le in range(0, __try_times):

                __logger.info(str((le + 1)) + "times," + "Afferent parameter:win_title:" + str(win_title))

                dicResult = ubpa.base_cs_dll.dllWinMaxmize(win_title,win_text)
                stringRst = dicResult["win_maxmize"]
                if stringRst == 1:
                    __logger.info(str((le + 1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != 1:
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = dicResult["win_maxmize"]
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[win_maxmize_cs]")


# #窗口最小化
def do_win_minimize(win_title="",win_text=None):
    __logger.info(u"Afferent parameter:win_title:" + str(win_title))
    __logger.echo_msg(u"Ready to execute[win_minmize_cs]")

    iresult = IResult()
    iresult.status = 0

    try:
        dicResult = ubpa.base_cs_dll.dllWinMinmize(win_title,win_text)
        stringRst = dicResult["win_minmize"]
        if stringRst != 1:

            for le in range(0, __try_times):

                __logger.info(str((le + 1)) + "times," + "Afferent parameter:win_title:" + str(win_title))

                dicResult = ubpa.base_cs_dll.dllWinMinmize(win_title,win_text)
                stringRst = dicResult["win_minmize"]
                if stringRst == 1:
                    __logger.info(str((le + 1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != 1:
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = dicResult["win_minmize"]
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[win_minmize_cs]")


# #select标签选择某一个选项
def do_cs_select(win_title="",win_text="",target=None,select_sring=""):
    __logger.info(u"Afferent parameter:select_sring:" + str(select_sring))
    __logger.echo_msg(u"Ready to execute[do_cs_select]")

    iresult = IResult()
    iresult.status = 0

    try:
        dicResult = ubpa.base_cs_dll.dllControlCommand(win_title,win_text,target,select_sring)
        stringRst = dicResult["control_command"]
        if stringRst != 1:

            for le in range(0, __try_times):

                __logger.info(str((le + 1)) + "times," + "Afferent parameter:select_sring:" + str(select_sring))

                dicResult = ubpa.base_cs_dll.dllControlCommand(win_title,win_text,target,select_sring)
                stringRst = dicResult["control_command"]
                if stringRst == 1:
                    __logger.info(str((le + 1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != 1:
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = dicResult["control_command"]
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[do_cs_select]")


def do_win_title_list():
    __logger.echo_msg(u"Ready to execute[win_title_list]")

    iresult = IResult()
    iresult.status = 0

    try:
        dicResult = ubpa.base_cs_dll.getWinList()
        stringRst = dicResult["winlist"]
        if stringRst == "":  # 表示没有得到窗口标题列表

            for le in range(0, __try_times):

                dicResult = ubpa.base_cs_dll.getWinList()
                stringRst = dicResult["winlist"]
                if stringRst != "":
                    __logger.info(str((le + 1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst == "":
            __logger.info(u"Interface returns error information:" + str(stringRst))

        iresult.obj = dicResult["winlist"]
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[win_title_list]")






