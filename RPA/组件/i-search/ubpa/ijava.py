# -*- coding: utf-8 -*-

from ctypes import *
from ubpa.ilog import ILog
import json
import ubpa.encrypt as encrypt
from ubpa.ierror import *
import time
from ubpa.iconstant import *
import ubpa.iie as iie
import ubpa.ics as ics
import ubpa.iwin as iwin
import ubpa.iimg as img

#dll = cdll.LoadLibrary("RpaAccessBridge.dll")
dll = cdll.LoadLibrary("../Com.Isearch.Func.Java/RpaAccessBridge.dll")


__logger = ILog(__file__)

def set_element_val(program=None,title=None,className=None,selector=None,text=None,waitfor=WAIT_FOR):

    __logger.debug('[set_element_val] Set text start')
    try:
        text = encrypt.decrypt(str(text))
        param = get_jsondata(program,title,className,selector,text=text)
        starttime = time.time()
        while True:
            return_data = dll.setElementValue(param)
            return_data = reverse_data(return_data)

            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if retCode == 1:
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + retError)
                    raise Exception(retError)
                __logger.debug(r'Attempt Failure - Wait for Attempt ' + retError)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e


def get_element_val(program=None, title=None, className=None, selector=None, waitfor=WAIT_FOR):

    __logger.debug('[get_element_val] Get the element value to start')
    try:
        param = get_jsondata(program,title,className,selector)
        starttime = time.time()
        while True:
            return_data = dll.getElementValue(param)
            return_data = reverse_data(return_data)

            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if retCode == 1:
                __logger.debug(r'get_element_val result ' + str(return_data["value"]))
                return return_data["value"]
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + retError)
                    raise Exception(retError)
                __logger.debug(r'Attempt Failure - Wait for Attempt ' + retError)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e


def click_element(program=None, title=None, className=None, selector=None, async=None, waitfor=WAIT_FOR):

    __logger.debug('[click_element] Start clicking elements ')
    try:
        param = get_jsondata(program, title, className, selector, async=async)
        starttime = time.time()
        while True:
            return_data = dll.clickElement(param)
            return_data = reverse_data(return_data)

            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if retCode == 1:
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + retError)
                    raise Exception(retError)
                __logger.debug(r'Attempt Failure - Wait for Attempt ' + retError)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e

def set_element_checked_state(program=None, title=None, className=None, selector=None,async=None,checkedState=None,waitfor=WAIT_FOR):

    __logger.debug('[set_element_checked_state] Start setting Checkbox check status')
    try:
        param = get_jsondata(program, title, className, selector, async=async, checkedState=checkedState)
        starttime = time.time()
        while True:
            return_data = dll.setElementCheckedState(param)
            return_data = reverse_data(return_data)

            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if retCode == 1:
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + retError)
                    raise Exception(retError)
                __logger.debug(r'Attempt Failure - Wait for Attempt ' + retError)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e

def set_element_focus(program=None,title=None,className=None,selector=None,waitfor=WAIT_FOR):

    __logger.debug('[set_element_focus] Start Setting element focus')
    try:
        param = get_jsondata(program, title, className, selector)
        starttime = time.time()
        while True:
            return_data = dll.setElementFocus(param)
            return_data = reverse_data(return_data)

            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if retCode == 1:
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + retError)
                    raise Exception(retError)
                __logger.debug(r'Attempt Failure - Wait for Attempt ' + retError)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e

def get_element_items(program=None,title=None,className=None,selector=None,waitfor=WAIT_FOR):

    __logger.debug('[get_element_items] Get the all selection of Select')
    try:
        param = get_jsondata(program, title, className, selector)
        starttime = time.time()
        while True:
            return_data = dll.getElementItems(param)
            return_data = reverse_data(return_data)

            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if retCode == 1:
                __logger.debug(r'get_element_items result ' + str(return_data["items"]))
                return return_data["items"]
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + retError)
                    raise Exception(retError)
                __logger.debug(r'Attempt Failure - Wait for Attempt ' + retError)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e

def get_element_selected_items(program=None,title=None,className=None,selector=None,waitfor=WAIT_FOR):

    __logger.debug('[get_element_selected_items]Get the current selection of Select')
    try:
        param = get_jsondata(program, title, className, selector)
        starttime = time.time()
        while True:
            return_data = dll.getElementSelectedItem(param)
            return_data = reverse_data(return_data)

            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if retCode == 1:
                __logger.debug(r'get_element_selected_items result ' + str(return_data["selectedItem"]))
                return return_data["selectedItem"]
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + retError)
                    raise Exception(retError)
                __logger.debug(r'Attempt Failure - Wait for Attempt ' + retError)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e


def set_element_selected_item(program=None,title=None,className=None,selector=None,itemText=None,waitfor=WAIT_FOR):

    __logger.debug('[set_element_selected_item] Set current option')
    try:
        param = get_jsondata(program, title, className, selector, itemText=itemText)
        starttime = time.time()
        while True:
            return_data = dll.setElementSelectedItem(param)
            return_data = reverse_data(return_data)

            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if retCode == 1:
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + retError)
                    raise Exception(retError)
                __logger.debug(r'Attempt Failure - Wait for Attempt ' + retError)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e

def get_element_text(program=None,title=None,className=None,selector=None,waitfor=WAIT_FOR):

    __logger.debug('[get_element_text] Start getting element text')
    try:
        param = get_jsondata(program, title, className, selector)
        starttime = time.time()
        while True:
            return_data = dll.getElementText(param)
            return_data = reverse_data(return_data)

            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if retCode == 1:
                __logger.debug(r'get_element_text result ' + str(return_data["texts"]))
                return return_data["texts"]  #得到的是一个json格式的数据
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + retError)
                    raise Exception(retError)
                __logger.debug(r'Attempt Failure - Wait for Attempt ' + retError)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e

def do_click_pos(program=None, title=None, className=None, selector=None, async=None, button='left',
                 curson='center',offsetX=0,offsetY=0,times=1,waitfor=WAIT_FOR,run_mode='unctrl'):

    __logger.debug('Click element operation:[' + str(title) + '][' + str(selector) + ']')
    try:
        if 'ctrl' == run_mode:
            click_element(program=program, title=title, className=className, selector=selector, async=async, waitfor=waitfor)
        else:
            if title != None and title.strip() != '':
                ''''如果窗口不活跃状态'''
                if not iwin.do_win_is_active(title):
                    iwin.do_win_activate(win_title=title, waitfor=waitfor)

            starttime = time.time()
            while True:
                param = get_jsondata(program, title, className, selector, async=async)
                return_data = dll.getRectangleFromElem(param)
                return_data = reverse_data(return_data)

                if int(return_data["retCode"]) == 1:
                    __logger.debug('Original position:'+str(return_data["x"])+" y:"+str(return_data["y"]))
                    __logger.debug('Original size:'+str(return_data["width"])+" y:"+str(return_data["height"]))
                    X, Y = iie.do_get_pos(return_data["x"], return_data["y"], return_data["width"],
                                      return_data["height"], curson, offsetX, offsetY,pos_scale='yes')


                    ics._mouse_click_cs(button, X, Y, 1, times)
                    return True
                else:
                    runtime = time.time() - starttime
                    if runtime >= waitfor:
                        __logger.debug('Operation timeout:[' + str(title) + '][' + str(selector) + ']')
                        raise Au3ExecError('Click element error:[' + str(title) + '][' + str(selector) + ']')
                    __logger.debug('Attempt Failure - Wait for Attempt:[' + str(title) + '][' + str(selector) + ']')
                    time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e


def do_moveto_pos(program=None, title=None, className=None, selector=None, async=None, curson='center',
                  offsetX=0, offsetY=0, waitfor=WAIT_FOR):
    __logger.debug('Move to pos:[' + str(title) + '][' + str(selector) + ']')
    try:
        if title != None and title.strip() != '':
            ''''如果窗口不活跃状态'''
            if not iwin.do_win_is_active(title):
                iwin.do_win_activate(win_title=title, waitfor=waitfor)

        starttime = time.time()
        while True:
            param = get_jsondata(program, title, className, selector, async=async)
            return_data = dll.getRectangleFromElem(param)
            return_data = reverse_data(return_data)

            if int(return_data["retCode"]) == 1:

                X, Y = iie.do_get_pos(return_data["x"], return_data["y"], return_data["width"],
                                  return_data["height"], curson, offsetX, offsetY,pos_scale='yes')
                __logger.debug('x:'+str(X)+" y:"+str(Y))
                ics._mouse_move_cs(X, Y, 1)
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug('Operation timeout:[' + str(title) + '][' + str(selector) + ']')
                    raise Au3ExecError('Move to pos error:[' + str(title) + '][' + str(selector) + ']')
                __logger.debug('Attempt Failure - Wait for Attempt:[' + str(title) + '][' + str(selector) + ']')
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e





def get_jsondata(program=None,title=None,className=None,selector=None,text=None,async=None,checkedState=None,itemText=None):
    param = '{"activite": "","target": {"program":"","title":"","className":"","hierarchy":"","async":""},' \
            '"input": {"text":"","checkedState":"","itemText":""}}'
    pjson = json.loads(param)

    if program != None:
        pjson["target"]["program"] = program
    if title != None:
        pjson["target"]["title"] = title
    if className != None:
        pjson["target"]["className"] = className

    pjson["target"]["hierarchy"] = selector
    if async != None:
        pjson["target"]["async"] = async

    if text != None:
        pjson["input"]["text"] = text
    if checkedState != None:
        pjson["input"]["checkedState"] = checkedState
    if itemText != None:
        pjson["input"]["itemText"] = itemText

    return json.dumps(pjson, ensure_ascii=False)

def reverse_data(param):

    string_data = string_at(param, -1).decode('utf-8')
    return json.loads(string_data)

def get_element_rect(program=None, title=None, className=None, selector=None, async=None, curson=None,offsetX=0,offsetY=0,waitfor=WAIT_FOR):

    __logger.debug('get_element_rect:[' + str(title) + '][' + str(selector) + ']')
    try:
        # if title != None and title.strip() != '':
        #     ''''如果窗口不活跃状态'''
        #     if not iwin.do_win_is_active(title):
        #         iwin.do_win_activate(win_title=title, waitfor=waitfor)

        starttime = time.time()
        while True:
            param = get_jsondata(program, title, className, selector, async=async)
            return_data = dll.getRectangleFromElem(param)
            return_data = reverse_data(return_data)

            if int(return_data["retCode"]) == 1:

                if curson != None and curson != "":
                    curson_x, curson_y = iie.do_get_pos(left=return_data["x"], top=return_data["y"],width=return_data["width"],
                                                        height=return_data["height"], curson=curson, offsetX=offsetX,offsetY=offsetY, pos_scale='yes')

                    return curson_x, \
                           curson_y, \
                           return_data["width"], \
                           return_data["height"]

                else:
                    return return_data["x"], \
                           return_data["y"], \
                           return_data["width"], \
                           return_data["height"]

            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug('Operation timeout:[' + str(title) + '][' + str(selector) + ']')
                    raise Au3ExecError('Move to pos error:[' + str(title) + '][' + str(selector) + ']')
                __logger.debug('Attempt Failure - Wait for Attempt:[' + str(title) + '][' + str(selector) + ']')
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e


def capture_element_img(program=None, title=None, className=None, selector=None, async=None, in_img_path=None,waitfor=WAIT_FOR):

    try:
        curson_x,curson_y,width,height = get_element_rect(program=program, title=title, className=className, selector=selector, async=async, curson='lefttop')

        in_img_path = img.capture_image(win_title=title, win_text="", in_img_path=in_img_path,left_indent=curson_x, top_indent=curson_y, width=width, height=height,waitfor=waitfor)

        return in_img_path
    except Exception as e:
        raise e

