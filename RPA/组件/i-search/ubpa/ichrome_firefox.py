# -*- coding: utf-8 -*-
'''
Created on 2018年8月22日

@author: ibm
'''

from ctypes import *
from ubpa.ilog import ILog
import json
import ubpa.encrypt as encrypt
from ubpa.ierror import *
import time
import platform
import winreg
from ubpa.iconstant import *
from ubpa import iwin
import ubpa.ics as ics
import ubpa.iimg as img



dll_chrome = cdll.LoadLibrary("..\..\plugin\Com.Isearch.Extension.Chrome\RpaChromeInterface.dll")
dll_firefox = cdll.LoadLibrary("..\..\plugin\Com.Isearch.Extension.Firefox\RpaFirefoxInterface.dll")
# dll_chrome = cdll.LoadLibrary("RpaChromeInterface.dll")
# dll_firefox = cdll.LoadLibrary("RpaFirefoxInterface.dll")
__logger = ILog(__file__)

def get_element_val_chrome(attrMap=None,index=0,tagName=None,title=None,url=None,waitfor=WAIT_FOR):
    '''
    获取chrome元素的值

        attrMap:元素属性
        index:搜索游标，暂时默认为0
        tagName:元素类型
        title:元素所在页面标题(如果存在)
        url:元素所在页面url(如果不存在title)
        waitfor:延时

    '''

    __logger.debug('[get_element_val_chrome] Get element value start')
    try:
        param = get_jsondata(attrMap,index,tagName,title,url)
        starttime = time.time()
        while True:
            return_data = dll_chrome.getElementValue(param)
            return_data = reverse_data(return_data)
            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if retCode == 1:
                __logger.debug(r'get_element_val_chrome  result ' + str(return_data["value"]))
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

def get_element_val_firefox(attrMap=None,index=0,tagName=None,title=None,url=None,waitfor=WAIT_FOR):
    '''
    获取firefox元素的值

        attrMap:元素属性
        index:搜索游标，暂时默认为0
        tagName:元素类型
        title:元素所在页面标题(如果存在)
        url:元素所在页面url(如果不存在title)
        waitfor:延时
    '''

    __logger.debug('[get_element_val_firefox] get element val start')
    try:
        param = get_jsondata(attrMap,index,tagName,title,url)
        starttime = time.time()
        while True:
            return_data = dll_firefox.getElementValue(param)
            return_data = reverse_data(return_data)
            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if retCode == 1:
                __logger.debug(r'get_element_val_firefox  result ' + str(return_data["value"]))
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

def set_element_val_chrome(attrMap=None,index=0,tagName=None,title=None,url=None,text=None,waitfor=WAIT_FOR):
    '''
    设置chrome元素值
        attrMap:元素属性
        index:搜索游标，暂时默认为0
        tagName:元素类型
        title:元素所在页面标题(如果存在)
        url:元素所在页面url(如果不存在title)
        text:需要设置的元素值
        waitfor:延时
    '''

    __logger.debug('[set_element_val_chrome] set element val start')
    try:
        text = encrypt.decrypt(str(text))
        param = get_jsondata(attrMap,index,tagName,title,url,text=text)
        starttime = time.time()
        while True:
            return_data = dll_chrome.setElementValue(param)
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

def set_element_val_firefox(attrMap=None,index=0,tagName=None,title=None,url=None,text=None,waitfor=WAIT_FOR):
    '''
    设置firefox元素值
        attrMap:元素属性
        index:搜索游标，暂时默认为0
        tagName:元素类型
        title:元素所在页面标题(如果存在)
        url:元素所在页面url(如果不存在title)
        text:需要设置的元素值
        waitfor:延时
    '''

    __logger.debug('[set_element_val_firefox] set element val start')
    try:
        text = encrypt.decrypt(str(text))
        param = get_jsondata(attrMap,index,tagName,title,url,text=text)
        print(param)
        starttime = time.time()
        while True:
            return_data = dll_firefox.setElementValue(param)
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

def click_element_chrome(attrMap=None,index=0,tagName=None,title=None,url=None,waitfor=WAIT_FOR):
    '''
    chrome鼠标点击元素
        attrMap:元素属性
        index:搜索游标，暂时默认为0
        tagName:元素类型
        title:元素所在页面标题(如果存在)
        url:元素所在页面url(如果不存在title)

    '''

    __logger.debug('[click_element_chrome] click element start')
    try:
        param = get_jsondata(attrMap,index,tagName,title,url)
        starttime = time.time()
        while True:
            return_data = dll_chrome.clickElement(param)
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

def click_element_firefox(attrMap=None,index=0,tagName=None,title=None,url=None,waitfor=WAIT_FOR):
    '''
    firefox鼠标点击元素
        attrMap:元素属性
        index:搜索游标，暂时默认为0
        tagName:元素类型
        title:元素所在页面标题(如果存在)
        url:元素所在页面url(如果不存在title)

    '''

    __logger.debug('[click_element_firefox]click element start')
    try:
        param = get_jsondata(attrMap,index,tagName,title,url)
        starttime = time.time()
        while True:
            return_data = dll_firefox.clickElement(param)
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

def set_element_checked_state_chrome(attrMap=None,index=0,tagName=None,title=None,url=None,checkedState=None,waitfor=WAIT_FOR):
    '''
    chrome设置Checkbox选中状态
          attrMap:元素属性
          index:搜索游标，暂时默认为0
          tagName:元素类型
          title:元素所在页面标题(如果存在)
          url:元素所在页面url(如果不存在title)
          checkedState:选中状态(1或者0)
      '''
    __logger.debug('[set_element_checked_state_chrome] set Checkbox checked state')
    try:
        if checkedState == "check":
            checkedState = 1
        else:
            checkedState = 0
        param = get_jsondata(attrMap,index,tagName,title,url, checkedState=checkedState)
        starttime = time.time()
        while True:
            return_data = dll_chrome.setElementCheckedState(param)
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

def set_element_checked_state_firefox(attrMap=None,index=0,tagName=None,title=None,url=None,checkedState=None,waitfor=WAIT_FOR):
    '''
    firefox设置Checkbox选中状态
          attrMap:元素属性
          index:搜索游标，暂时默认为0
          tagName:元素类型
          title:元素所在页面标题(如果存在)
          url:元素所在页面url(如果不存在title)
          checkedState:选中状态(1或者0)
      '''
    __logger.debug('[set_element_checked_state_firefox] set Checkbox checked state ')
    try:
        if checkedState == "check":
            checkedState = 1
        else:
            checkedState = 0
        param = get_jsondata(attrMap,index,tagName,title,url, checkedState=checkedState)
        starttime = time.time()
        while True:
            return_data = dll_firefox.setElementCheckedState(param)
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

def set_element_focus_chrome(attrMap=None,index=0,tagName=None,title=None,url=None,waitfor=WAIT_FOR):
    '''
    chrome设置元素焦点
          attrMap:元素属性
          index:搜索游标，暂时默认为0
          tagName:元素类型
          title:元素所在页面标题(如果存在)
          url:元素所在页面url(如果不存在title)

    '''

    __logger.debug('[set_element_focus_chrome] set element focus')
    try:
        param = get_jsondata(attrMap,index,tagName,title,url)
        starttime = time.time()
        while True:
            return_data = dll_chrome.setElementFocus(param)
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


def set_element_focus_firefox(attrMap=None, index=0, tagName=None, title=None, url=None, waitfor=WAIT_FOR):
    '''
    firefox设置元素焦点
          attrMap:元素属性
          index:搜索游标，暂时默认为0
          tagName:元素类型
          title:元素所在页面标题(如果存在)
          url:元素所在页面url(如果不存在title)

    '''

    __logger.debug('[set_element_focus_firefoxe] set element focus')
    try:
        param = get_jsondata(attrMap, index, tagName, title, url)
        starttime = time.time()
        while True:
            return_data = dll_firefox.setElementFocus(param)
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

def get_element_items_chrome(attrMap=None, index=0, tagName=None, title=None, url=None,waitfor=WAIT_FOR):
    '''
    chrome得到Select的全部选择项
          attrMap:元素属性
          index:搜索游标，暂时默认为0
          tagName:元素类型
          title:元素所在页面标题(如果存在)
          url:元素所在页面url(如果不存在title)

    '''

    __logger.debug('[get_element_items_chrome] get element items')
    try:
        param = get_jsondata(attrMap, index, tagName, title, url)
        starttime = time.time()
        while True:
            return_data = dll_chrome.getElementItems(param)
            return_data = reverse_data(return_data)

            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if retCode == 1:
                __logger.debug(r'get_element_items  result ' + str(return_data["items"]))
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

def get_element_items_firefox(attrMap=None, index=0, tagName=None, title=None, url=None,waitfor=WAIT_FOR):
    '''
    firefox得到Select的全部选择项
          attrMap:元素属性
          index:搜索游标，暂时默认为0
          tagName:元素类型
          title:元素所在页面标题(如果存在)
          url:元素所在页面url(如果不存在title)

    '''

    __logger.debug('[get_element_items_firefox] get element items')
    try:
        param = get_jsondata(attrMap, index, tagName, title, url)
        starttime = time.time()
        while True:
            return_data = dll_firefox.getElementItems(param)
            return_data = reverse_data(return_data)

            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if retCode == 1:
                __logger.debug(r'get_element_items  result ' + str(return_data["items"]))
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

def get_element_selected_items_chrome(attrMap=None, index=0, tagName=None, title=None, url=None,waitfor=WAIT_FOR):
    '''
    chrome得到Select的当前选中项
          attrMap:元素属性
          index:搜索游标，暂时默认为0
          tagName:元素类型
          title:元素所在页面标题(如果存在)
          url:元素所在页面url(如果不存在title)

    '''

    __logger.debug('[get_element_selected_items_chrome] get element selected items')
    try:
        param = get_jsondata(attrMap, index, tagName, title, url)
        starttime = time.time()
        while True:
            return_data = dll_chrome.getElementSelectedItem(param)
            return_data = reverse_data(return_data)

            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if retCode == 1:
                __logger.debug(r'get_element_selected_items  result ' + str(return_data["selectedItem"]))
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


def get_element_selected_items_firefox(attrMap=None, index=0, tagName=None, title=None, url=None,waitfor=WAIT_FOR):
    '''
    firefox得到Select的当前选中项
          attrMap:元素属性
          index:搜索游标，暂时默认为0
          tagName:元素类型
          title:元素所在页面标题(如果存在)
          url:元素所在页面url(如果不存在title)

    '''

    __logger.debug('[get_element_selected_items_firefox]get element selected items')
    try:
        param = get_jsondata(attrMap, index, tagName, title, url)
        starttime = time.time()
        while True:
            return_data = dll_firefox.getElementSelectedItem(param)
            return_data = reverse_data(return_data)

            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if retCode == 1:
                __logger.debug(r'get_element_selected_items  result ' + str(return_data["selectedItem"]))
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


def set_element_selected_item_chrome(attrMap=None, index=0, tagName=None, title=None, url=None,itemText=None,waitfor=WAIT_FOR):
    '''
    chrome设置Select的选中项
          attrMap:元素属性
          index:搜索游标，暂时默认为0
          tagName:元素类型
          title:元素所在页面标题(如果存在)
          url:元素所在页面url(如果不存在title)
          itemText:选中项的值

    '''

    __logger.debug('[set_element_selected_item_chrome] set element selected item')
    try:
        param = get_jsondata(attrMap, index, tagName, title, url, itemText=itemText)
        starttime = time.time()
        while True:
            return_data = dll_chrome.setElementSelectedItem(param)
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


def set_element_selected_item_firefox(attrMap=None, index=0, tagName=None, title=None, url=None,itemText=None,waitfor=WAIT_FOR):
    '''
    firefox设置Select的选中项
          attrMap:元素属性
          index:搜索游标，暂时默认为0
          tagName:元素类型
          title:元素所在页面标题(如果存在)
          url:元素所在页面url(如果不存在title)
          itemText:选中项的值

    '''

    __logger.debug('[set_element_selected_item_firefox]set element selected item')
    try:
        param = get_jsondata(attrMap, index, tagName, title, url, itemText=itemText)
        starttime = time.time()
        while True:
            return_data = dll_firefox.setElementSelectedItem(param)
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


def get_element_rect_chrome(attrMap=None,index=0,tagName=None,title=None,url=None,curson=None,offsetX=0,offsetY=0,waitfor=WAIT_FOR):
    '''
       chrome获取元素的位置
             attrMap:元素属性
             index:搜索游标，暂时默认为0
             tagName:元素类型
             title:元素所在页面标题(如果存在)
             url:元素所在页面url(如果不存在title)

    '''

    __logger.debug('[get_element_rect_chrome] Get element location')
    try:
        # if title != None and title.strip() != '':
        #     ''''如果窗口不活跃状态'''
        #     if not iwin.do_win_is_active(title):
        #         iwin.do_win_activate(win_title=title, waitfor=waitfor)

        starttime = time.time()
        while True:
            param = get_jsondata(attrMap, index, tagName,title, url)
            result = dll_chrome.getElementRect(param)
            return_data = reverse_data(result)
            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if int(retCode) == 1:

                if curson != None and curson != "":
                    curson_x, curson_y = do_get_pos(left=return_data["x"], top=return_data["y"], width=return_data["width"],
                                                    height=return_data["height"], curson=curson, offsetX=offsetX,offsetY=offsetY)

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
                    __logger.debug(r'Operation timeout ' + retError)
                    raise Exception(retError)
                __logger.debug(r'Attempt Failure - Wait for Attempt ' + retError)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e


def get_element_rect_firefox(attrMap=None,index=0,tagName=None,title=None,url=None,curson=None,offsetX=0,offsetY=0,waitfor=WAIT_FOR):
    '''
       firefox获取元素的位置
             attrMap:元素属性
             index:搜索游标，暂时默认为0
             tagName:元素类型
             title:元素所在页面标题(如果存在)
             url:元素所在页面url(如果不存在title)

    '''

    __logger.debug('[get_element_rect_firefox] Get element location')
    try:
        # if title != None and title.strip() != '':
        #     ''''如果窗口不活跃状态'''
        #     if not iwin.do_win_is_active(title):
        #         iwin.do_win_activate(win_title=title, waitfor=waitfor)

        starttime = time.time()
        while True:
            param = get_jsondata(attrMap, index, tagName,title, url)
            result = dll_firefox.getElementRect(param)
            return_data = reverse_data(result)
            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if int(retCode) == 1:

                if curson != None and curson != "":
                    curson_x, curson_y = do_get_pos(left=return_data["x"], top=return_data["y"], width=return_data["width"],
                                                    height=return_data["height"], curson=curson, offsetX=offsetX,offsetY=offsetY)

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
                    __logger.debug(r'Operation timeout ' + retError)
                    raise Exception(retError)
                __logger.debug(r'Attempt Failure - Wait for Attempt ' + retError)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e



def do_click_pos_chrome(attrMap=None, index=0, tagName=None, title=None,url=None,button='left',curson='center',offsetX=0,offsetY=0,
                        times=1,waitfor=WAIT_FOR,run_mode='unctrl'):
    '''
       chrome点击元素操作
             attrMap:元素属性
             index:搜索游标，暂时默认为0
             tagName:元素类型
             title:元素所在页面标题(如果存在)
             url:元素所在页面url(如果不存在title)
             button: 鼠标点击操作 左击或者右击
             offsetX: x轴
             offsetY: y轴

    '''

    __logger.debug('[do_click_pos_chrome] Click element')
    try:
        if 'ctrl' == run_mode:
            click_element_chrome(attrMap=attrMap,index=index,tagName=tagName,title=title,url=url,waitfor=waitfor)
        else:
            if title != None and title.strip() != '':
                ''''如果窗口不活跃状态'''
                if not iwin.do_win_is_active(title):
                    iwin.do_win_activate(win_title=title, waitfor=waitfor)

            starttime = time.time()
            while True:
                param = get_jsondata(attrMap, index, tagName, title, url)
                result = dll_chrome.getElementRect(param)
                return_data = reverse_data(result)
                print(return_data)
                retCode = return_data["retCode"]
                retError = return_data["retError"]

                if int(retCode) == 1:
                    X, Y = do_get_pos(return_data["x"], return_data["y"], return_data["width"],
                                      return_data["height"], curson, offsetX, offsetY)
                    ics._mouse_click_cs(button, X, Y, 1, times)
                    return True
                else:
                    runtime = time.time() - starttime
                    if runtime >= waitfor:
                        __logger.debug(r'Operation timeout' + retError)
                        raise Exception(retError)
                    __logger.debug(r'Attempt Failure - Wait for Attempt ' + retError)
                    time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e


def do_click_pos_firefox(attrMap=None, index=0, tagName=None, title=None,url=None,button='left',curson='center',offsetX=0,
                         offsetY=0,times=1,waitfor=WAIT_FOR,run_mode='unctrl'):
    '''
       firefox点击元素操作
             attrMap:元素属性
             index:搜索游标，暂时默认为0
             tagName:元素类型
             title:元素所在页面标题(如果存在)
             url:元素所在页面url(如果不存在title)
             button: 鼠标点击操作 左击或者右击
             offsetX: x轴
             offsetY: y轴

    '''

    __logger.debug('[do_click_pos_firefox ]Click element')
    try:
        if 'ctrl' == run_mode:
            click_element_firefox(attrMap=attrMap, index=index, tagName=tagName, title=title, url=url, waitfor=waitfor)
        else:
            if title != None and title.strip() != '':
                ''''如果窗口不活跃状态'''
                if not iwin.do_win_is_active(title):
                    iwin.do_win_activate(win_title=title, waitfor=waitfor)

            starttime = time.time()
            while True:
                param = get_jsondata(attrMap, index, tagName, title, url)
                result = dll_firefox.getElementRect(param)
                return_data = reverse_data(result)
                print(return_data)
                retCode = return_data["retCode"]
                retError = return_data["retError"]

                if int(retCode) == 1:
                    X, Y = do_get_pos(return_data["x"], return_data["y"], return_data["width"],
                                      return_data["height"], curson, offsetX, offsetY)
                    ics._mouse_click_cs(button, X, Y, 1, times)
                    return True
                else:
                    runtime = time.time() - starttime
                    if runtime >= waitfor:
                        __logger.debug(r'Operation timeout' + retError)
                        raise Exception(retError)
                    __logger.debug(r'Attempt Failure - Wait for Attempt ' + retError)
                    time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e




def do_moveto_pos_chrome(attrMap=None, index=0, tagName=None, title=None,url=None,curson='center',offsetX=0,offsetY=0,waitfor=WAIT_FOR):
    '''
       chrome鼠标移动操作
             attrMap:元素属性
             index:搜索游标，暂时默认为0
             tagName:元素类型
             title:元素所在页面标题(如果存在)
             url:元素所在页面url(如果不存在title)
             offsetX: x轴
             offsetY: y轴

    '''

    __logger.debug('[do_moveto_pos_chrome] Mouse move')
    try:
        if title != None and title.strip() != '':
            ''''如果窗口不活跃状态'''
            if not iwin.do_win_is_active(title):
                iwin.do_win_activate(win_title=title, waitfor=waitfor)

        starttime = time.time()
        while True:
            param = get_jsondata(attrMap, index, tagName, title, url)
            result = dll_chrome.getElementRect(param)
            return_data = reverse_data(result)
            print(return_data)
            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if int(retCode) == 1:

                X, Y = do_get_pos(return_data["x"], return_data["y"], return_data["width"],
                                  return_data["height"], curson, offsetX, offsetY)
                ics._mouse_move_cs(X, Y, 1)
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout' + retError)
                    raise Exception(retError)
                __logger.debug(r'Attempt Failure - Wait for Attempt ' + retError)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e

def do_moveto_pos_firefox(attrMap=None, index=0, tagName=None, title=None,url=None,curson='center',offsetX=0,offsetY=0,waitfor=WAIT_FOR):
    '''
       firefox鼠标移动操作
             attrMap:元素属性
             index:搜索游标，暂时默认为0
             tagName:元素类型
             title:元素所在页面标题(如果存在)
             url:元素所在页面url(如果不存在title)
             offsetX: x轴
             offsetY: y轴

    '''

    __logger.debug('[do_moveto_pos_firefox]Mouse move')
    try:
        if title != None and title.strip() != '':
            ''''如果窗口不活跃状态'''
            if not iwin.do_win_is_active(title):
                iwin.do_win_activate(win_title=title, waitfor=waitfor)

        starttime = time.time()
        while True:
            param = get_jsondata(attrMap, index, tagName, title, url)
            result = dll_firefox.getElementRect(param)
            return_data = reverse_data(result)
            print(return_data)
            retCode = return_data["retCode"]
            retError = return_data["retError"]

            if int(retCode) == 1:

                X, Y = do_get_pos(return_data["x"], return_data["y"], return_data["width"],
                                  return_data["height"], curson, offsetX, offsetY)
                ics._mouse_move_cs(X, Y, 1)
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout' + retError)
                    raise Exception(retError)
                __logger.debug(r'Attempt Failure - Wait for Attempt ' + retError)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e




def get_jsondata(attrMap=None,index=0,tagName=None,title=None,url=None,text=None,itemText=None,checkedState=None):
    param = {"activite" : "","input": {"text": "", "checkedState" : "","itemText" : ""},"target" : {"attrMap" : "","index" : "","tagName" : "","title" : "","url" : "" }}

    if attrMap != None:
        param["target"]["attrMap"] = attrMap
    if title != None:
        param["target"]["title"] = title
    else:
        param["target"]["url"] = url
    if index != None:
        param["target"]["index"] = index
    if tagName != None:
        param["target"]["tagName"] = tagName
    if text != None:
        param["input"]["text"] = text
    if itemText != None:
        param["input"]["itemText"] = itemText
    if checkedState != None:
        param["input"]["checkedState"] = checkedState
    return json.dumps(param, ensure_ascii=False)

def reverse_data(param):

    string_data = string_at(param, -1).decode('utf-8')
    return json.loads(string_data)


def do_get_pos(left=None, top=None, width=None, height=None, curson=None, offsetX=0, offsetY=0,
               pos_scale='no'):  # left,top表示左上角坐标
    X = None
    Y = None
    curs = str(curson).lower()
    if pos_scale == 'yes':
        '''java 时计算的dpi是保存到注册表中的'''
        sc = get_reg_dpi()
        __logger.debug('sc:' + str(sc))
        left = left / sc
        top = top / sc
        width = width / sc
        height = height / sc
        __logger.debug('after shift position:left:' + str(left) + " top:" + str(top))

    try:
        if curs == "center":
            X = left + width / 2 + offsetX
            Y = top + height / 2 + offsetY
        if curs == "lefttop":
            X = left + offsetX
            Y = top + offsetY
        if curs == "righttop":
            X = left + width + offsetX
            Y = top + offsetY
        if curs == "leftbottom":
            X = left + offsetX
            Y = top + height + offsetY
        if curs == "rightbottom":
            X = left + width + offsetX
            Y = top + height + offsetY

        return X, Y
    except Exception as e:
        raise e


def get_reg_dpi():
    dpi = 1
    try:
        platform_name = platform.platform()
        __logger.debug('platform:' + str(platform_name))
        if 'Windows-7' in platform_name:
            return dpi
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop\WindowMetrics")
        i = 0
        while 1:
            name, value, type = winreg.EnumValue(key, i)
            if ('AppliedDPI' in repr(name)):
                dpi = value
                dpi = dpi / 96
                break
            i += 1
    except Exception as e:
        print(e)
    finally:
        return dpi

def capture_image_chrome(attrMap=None, index=0, tagName=None, title=None, url=None, in_img_path=None,waitfor=WAIT_FOR):

    try:
        curson_x, curson_y,width,height = get_element_rect_chrome(attrMap=attrMap, index=index, tagName=tagName, title=title, url=url, curson='lefttop')

        in_img_path = img.capture_image(win_title=title, win_text="", in_img_path=in_img_path,left_indent=curson_x, top_indent=curson_y, width=width, height=height,waitfor=waitfor)

        return in_img_path
    except Exception as e:
        raise e

def capture_image_firefox(attrMap=None, index=0, tagName=None, title=None, url=None, in_img_path=None,waitfor=WAIT_FOR):

    try:
        curson_x, curson_y,width,height = get_element_rect_firefox(attrMap=attrMap, index=index, tagName=tagName, title=title, url=url, curson='lefttop')

        in_img_path = img.capture_image(win_title=title, win_text="", in_img_path=in_img_path,left_indent=curson_x, top_indent=curson_y, width=width, height=height,waitfor=waitfor)

        return in_img_path
    except Exception as e:
        raise e