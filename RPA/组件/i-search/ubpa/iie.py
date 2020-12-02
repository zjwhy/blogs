# -*- coding: utf-8 -*-
from ctypes import *
import datetime
import json
import platform
import time
from ubpa import iwin
from ubpa.iconstant import *
from ubpa.ierror import *
from ubpa.ilog import ILog
import winreg

import win32api
import win32con

import ubpa.encrypt as encrypt
import ubpa.ics as ics
import ubpa.iimg as img


#dll = cdll.LoadLibrary("UEBAIEWatcher.dll")
dll = cdll.LoadLibrary("../../bin/UEBAIEWatcher.dll")
#dll = cdll.LoadLibrary(r'D:\work\svn\isa\branches\ueba_5\makesetup\CdaSetupDate\bin\UEBAIEWatcher.dll')
__logger = ILog(__file__)

'''
打开网址
ie_path:ie浏览器地址
url:网址

'''
def open_url(ie_path="C:/Program Files (x86)/Internet Explorer/iexplore.exe",url=""):
    __logger.debug('Open URL:['+str(url)+']')
    try:
         path=ie_path+" "+url
         result=ics.run_app(path,work_path=None)
         if result == 0:
             errmsg = 'Open application error [' + path + '] '
             __logger.error(errmsg)
             raise AppOpenError(errmsg)
         return result
    except Exception as e:
        raise e



'''
获取页面元素属性内容
title:标题
selector:
'''
def get_text(title="",url="",selector="",waitfor=WAIT_FOR):
    __logger.debug('IE get text:['+str(title)+']['+str(selector)+']')
    text = None
    try:
        param = get_param(title,url,selector)
        starttime = time.time()
        while True:
            text = string_at(dll.getText(param), -1).decode('utf-8') 
            err = string_at(dll.getLastError(), -1).decode('utf-8')  
            if err  == "": 
                return text
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + err)
                    break
                __logger.debug(r'Attempt Failure - Wait for Attempt to Acquire' + err)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e
    finally:
        __logger.debug('IE get text:' + str(text))
        return text


'''
  获取元素的html
'''
def get_html(title="",url="",selector="",waitfor=WAIT_FOR):
    __logger.debug('IE get Html:['+str(title)+']['+str(selector)+']')
    text = None
    try:
        param = get_param(title,url,selector)
        starttime = time.time()
        while True:
            text = string_at(dll.getHtml(param), -1).decode('utf-8')
            err = string_at(dll.getLastError(), -1).decode('utf-8')
            if err  == "":
                return text
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout' + err)
                    break
                __logger.debug(r'Attempt Failure - Wait for Attempt to Acquire' + err)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e
    finally:
        __logger.debug('IE get Html:' + text)
        return text

'''
给页面赋值
title:标题
selector:查找路径
text:赋值的内容
'''
def set_text(title="",url="",selector="",text="",waitfor=WAIT_FOR):
    __logger.debug('IE set text:['+str(title)+']['+str(selector)+']['+str(text)+']')
    try:
        text = encrypt.decrypt(text)
        param = get_param(title,url,selector,text)
        starttime = time.time()
        while True:
            dll.setText(param)
            err = string_at(dll.getLastError(), -1).decode('utf-8')  
            if err  == "": 
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + err)
                    raise Exception(err)
                __logger.debug(r'Attempt Failure - Wait for Attempt to Acquire ' + err)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e 

'''
判断是否是所选文本
title:标题
selector:查找路径
text:要判断的值
'''
def exists_text(title="",url="",selector="",text="",waitfor=WAIT_FOR):
    __logger.debug('IE  is selected text:[' + str(title) + '][' + str(selector) + ']')
    exists=False
    try:
        param = get_param(title, url,selector,text)
        starttime = time.time()
        while True:
            stringtext=dll.existsText(param)
            err = string_at(dll.getLastError(), -1).decode('utf-8')
            if err  == "":
                if stringtext == 1:
                    __logger.debug('IE is selected text:1')
                    exists=True
                else:
                    __logger.debug('IE is selected text:0')
                    exists=False
                break
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + err)
                    break
                __logger.debug(r'Attempt Failure - Wait for Attempt to Acquire '+err)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e
    finally:
        return exists

'''
获取值
title:标题
selector:查找路径

'''
def get_val(title="",url="",selector="",waitfor=WAIT_FOR):
    __logger.debug('IE get value:[' + str(title) + '][' + str(selector) + ']')
    text = ""
    try:
        param = get_param(title, url,selector)
        starttime = time.time()
        while True:
            text = dll.getVal(param)
            err = string_at(dll.getLastError(), -1).decode('utf-8')
            if err == "":
                return text
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + err)
                    text = ""
                    break
                __logger.debug(r'Attempt Failure - Wait for Attempt to Acquire ' + err)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e
    finally:
        __logger.debug('get value is:'+str(text))


'''
判断是否是所选值
title:标题
selector:查找路径
text:要判断的值
'''
def exists_val(title="",url="",selector="",text="",waitfor=WAIT_FOR):
    __logger.debug('is selected value:[' + str(title) + '][' + str(selector) + ']')
    exists = False
    try:
        param = get_param(title, url,selector, text)
        starttime = time.time()
        while True:
            stringtext=dll.existsVal(param)
            err = string_at(dll.getLastError(), -1).decode('utf-8')
            if err == "":
                if stringtext == 1:
                    __logger.debug('IE is selected value:1')
                    exists=True
                else:
                    __logger.debug('IE is selected value:0')
                    exists=False
                break
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + err)
                    break
                __logger.debug(r'Attempt Failure - Wait for Attempt to Acquire ' + err)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e
    finally:
        return exists

'''
checkBox选中操作
title:标题
selector:查找路径
action:操作类型
'''

def do_check(title="",url="",selector="",action="check",waitfor=WAIT_FOR):
    __logger.debug('checkBox is selected:[' + str(title) + '][' + str(selector) + ']')
    try:
        param = get_param(title, url,selector,action=action)
        starttime = time.time()
        while True:
            dll.doCheck(param)
            err = string_at(dll.getLastError(), -1).decode('utf-8')
            if err == "":
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + err)
                    raise Exception(err)
                __logger.debug(r'Attempt Failure - Wait for Attempt to Acquire ' + err)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e

'''
多选框
title:标题
selector:查找路径
item:需要选中的值
itemmode:值的类型
'''

def do_select(title="",url="",selector="",item="",itemmode="",waitfor=WAIT_FOR):
    __logger.debug('Drop-down selection:[' + str(title) + '][' + str(selector) + ']')
    try:
        param = get_param(title,url,selector,item=item ,itemmode=itemmode )
        starttime = time.time()
        while True:
            dll.doSelect(param)
            err = string_at(dll.getLastError(), -1).decode('utf-8')
            if err == "":
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + err)
                    raise Exception(err)
                __logger.debug(r'Attempt Failure - Wait for Attempt to Acquire ' + err)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e


'''
单选框
title:标题
selector:查找路径

'''

def do_radio(title="",url="",selector="",waitfor=WAIT_FOR):
    __logger.debug('select radio:[' + str(title) + '][' + str(selector) + ']')
    try:
        param = get_param(title, url,selector)
        starttime = time.time()
        while True:
            dll.doRadio(param)
            err = string_at(dll.getLastError(), -1).decode('utf-8')
            if err == "":
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + err)
                    raise Exception(err)
                __logger.debug(r'Attempt Failure - Wait for Attempt to Acquire ' + err)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e

'''
点击元素操作
title:标题
selector:查找路径

'''

def do_click(title="",url="",selector="",waitfor=WAIT_FOR):
    __logger.debug('click element:[' + title + '][' + selector + ']')
    try:
        param = get_param(title, url,selector)
        starttime = time.time()
        while True:
            dll.doClick(param)
            err = string_at(dll.getLastError(), -1).decode('utf-8')
            if err == "":
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + err)
                    raise Exception(err)
                __logger.debug(r'Attempt Failure - Wait for Attempt to Acquire ' + err)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e

'''
双击元素操作
title:标题
selector:查找路径

'''

def do_double_click(title="",url="",selector="",waitfor=WAIT_FOR):
    __logger.debug('doubleclick element:[' + str(title) + '][' + str(selector) + ']')
    try:
        param = get_param(title, url,selector)
        starttime = time.time()
        while True:
            dll.doDoubleClick(param)
            err = string_at(dll.getLastError(), -1).decode('utf-8')
            if err == "":
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + err)
                    raise Exception(err)
                __logger.debug(r'Attempt Failure - Wait for Attempt to Acquire ' + err)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e


'''
模拟鼠标点击操作
title:标题
selector:查找路径

'''

def do_mouse_click(win_title="",title="",url="",selector="",waitfor=WAIT_FOR):
    __logger.debug('do_mouse_click:[' + str(title) + '][' + str(selector) + ']')
    try:
        ''''如果指定窗口'''
        if win_title != None and win_title.strip() != '':
            ''''如果窗口不活跃状态'''
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)
                
        param = get_param(title, url,selector)
        starttime = time.time()
        while True:
            dll.doMouseClick(param)
            err = string_at(dll.getLastError(), -1).decode('utf-8')
            if err == "":
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + err)
                    raise Exception(err)
                __logger.debug(r'Attempt Failure - Wait for Attempt to Acquire ' + err)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e


'''
模拟键盘输入操作
title:标题
selector:查找路径
text:需要输入的值
'''

def do_keypress(win_title="",title="",url="",selector="",text="",waitfor=WAIT_FOR):
    __logger.debug('do_keypress:[' + str(title) + '][' + str(selector) + '][' + str(text) + ']')
    try:
        ''''如果指定窗口'''
        if win_title != None and win_title.strip() != '':
            ''''如果窗口不活跃状态'''
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)
                
                
        text = encrypt.decrypt(text)
        param = get_param(title, url,selector,text)
        starttime = time.time()
        while True:
            dll.doKeypress(param)
            err = string_at(dll.getLastError(), -1).decode('utf-8')
            if err == "":
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug(r'Operation timeout ' + err)
                    raise Exception(err)
                __logger.debug(r'Attempt Failure - Wait for Attempt to Acquire ' + err)
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e


def do_click_pos(win_title=None,title=None,url=None,selector=None,button='left',curson='center',offsetX=0,offsetY=0,times=1,
                 waitfor=WAIT_FOR,run_mode='unctrl',scroll_view='no'):

    __logger.debug('do_click_pos:[' + str(title) + '][' + str(selector) + ']')
    try:
        if 'ctrl' == run_mode:
            do_click(title=win_title, url=url, selector=selector, waitfor=waitfor)
        else:
            if win_title != None and win_title.strip() != '':
                ''''如果窗口不活跃状态'''
                if not iwin.do_win_is_active(win_title):
                    iwin.do_win_activate(win_title=win_title, waitfor=waitfor)

            starttime = time.time()
            while True:
                param = get_param(title, url, selector)
                if scroll_view == 'yes':
                    dll.doScrollIntoView(param)
                result = dll.getElementRect(param)
                result_pos_json = string_at(result, -1).decode('utf-8')
                result_pos_dic = json.loads(result_pos_json)

                if int(result_pos_dic["retCode"]) == 1:

                    X, Y = do_get_pos(result_pos_dic["x"], result_pos_dic["y"], result_pos_dic["width"],
                                      result_pos_dic["height"], curson, offsetX, offsetY)

                    ics._mouse_click_cs(button, X, Y, 1, times)
                    return True
                else:
                    runtime = time.time() - starttime
                    if runtime >= waitfor:
                        __logger.debug('Operation timeout:[' + str(title) + '][' + str(selector) + ']')
                        raise Au3ExecError('do_click_pos error:[' + str(title) + '][' + str(selector) + ']')
                    __logger.debug('Attempt Failure - Wait for Attempt to Acquire:[' + str(title) + '][' + str(selector) + ']')
                    time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e


def do_moveto_pos(win_title=None,title=None,url=None,selector=None,curson='center',offsetX=0,offsetY=0,waitfor=WAIT_FOR):

    __logger.debug('do_moveto_pos:[' + str(title) + '][' + str(selector) + ']')
    try:
        if win_title != None and win_title.strip() != '':
            ''''如果窗口不活跃状态'''
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)

        starttime = time.time()
        while True:
            param = get_param(title, url, selector)
            result = dll.getElementRect(param)
            result_pos_json = string_at(result, -1).decode('utf-8')
            result_pos_dic = json.loads(result_pos_json)

            if int(result_pos_dic["retCode"]) == 1:

                X, Y = do_get_pos(result_pos_dic["x"], result_pos_dic["y"], result_pos_dic["width"],
                                  result_pos_dic["height"], curson, offsetX, offsetY)
                ics._mouse_move_cs(X, Y, 1)
                return True
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug('Operation timeout:[' + str(title) + '][' + str(selector) + ']')
                    raise Au3ExecError('do_moveto_pos error:[' + str(title) + '][' + str(selector) + ']')
                __logger.debug('Attempt Failure - Wait for Attempt to Acquire:[' + str(title) + '][' + str(selector) + ']')
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e

def get_element_rect(win_title=None,title=None,url=None,selector=None,curson=None,offsetX=0,offsetY=0,waitfor=WAIT_FOR):

    __logger.debug('get_element_rect:[' + str(title) + '][' + str(selector) + ']')
    try:
        # if win_title != None and win_title.strip() != '':
        #     ''''如果窗口不活跃状态'''
        #     if not iwin.do_win_is_active(win_title):
        #         iwin.do_win_activate(win_title=win_title, waitfor=waitfor)

        starttime = time.time()
        while True:
            param = get_param(title, url, selector)
            result = dll.getElementRect(param)
            result_pos_json = string_at(result, -1).decode('utf-8')
            result_pos_dic = json.loads(result_pos_json)

            if int(result_pos_dic["retCode"]) == 1:

                if curson != None and curson != "":
                    curson_x, curson_y = do_get_pos(left=result_pos_dic["x"], top=result_pos_dic["y"],width=result_pos_dic["width"],
                                                    height=result_pos_dic["height"], curson=curson, offsetX=offsetX,offsetY=offsetY)

                    return curson_x, \
                           curson_y, \
                           result_pos_dic["width"], \
                           result_pos_dic["height"]

                else:
                    return result_pos_dic["x"], \
                           result_pos_dic["y"], \
                           result_pos_dic["width"], \
                           result_pos_dic["height"]
               
            else:
                runtime = time.time() - starttime
                if runtime >= waitfor:
                    __logger.debug('get_element_rect [' + str(title) + '][' + str(selector) + ']')
                    raise Au3ExecError('IE get_element_rect [' + str(title) + '][' + str(selector) + ']')
                __logger.debug('Attempt Failure - Wait for Attempt to Acquire:[' + str(title) + '][' + str(selector) + ']')
                time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e

def get_param(title="",url="",selector="",text="",item="",itemmode="",action="", js="", pid=0):
    param = '{"activite":"","input":{"item":"","itemmode":"","text":"","action":""},"target":{"selector":"","title":"","url":""}}'
    pjson = json.loads(param)
    if selector != "":
        pjson["target"]["selector"] = selector
    if title != "":
        pjson["target"]["title"] = title
    if url != "":
        pjson["target"]["url"] = url
    if text != "":
        pjson["input"]["text"] = text  # 是否所选文本、设置文本，是否所选顺序，键盘输入
    if item != "":
        pjson["input"]["item"] = item #下拉选择
    if itemmode != "":
        pjson["input"]["itemmode"] = itemmode  # 下拉选择
    if action != "":
        pjson["input"]["action"] = action  #多选框设置
    if js != "":
        pjson["target"]["jscode"] = js
    if pid != 0:
        pjson["target"]["pid"] = pid  #多选框设置
    return json.dumps(pjson, ensure_ascii=False)


def do_get_pos(left=None,top=None,width=None,height=None,curson=None,offsetX=0,offsetY=0,pos_scale='no'): #left,top表示左上角坐标
    X = None
    Y = None
    curs = str(curson).lower()
    if pos_scale == 'yes':
        '''java 时计算的dpi是保存到注册表中的'''
        sc = get_reg_dpi()
        __logger.debug('sc:'+str(sc))
        left = left/sc
        top = top/sc 
        width = width/sc
        height = height/sc
        __logger.debug('Converted position:left:'+str(left)+" top:"+str(top))
    
     
    try:
        if curs == "center":
            X = left + width/2 + offsetX
            Y = top + height/2 + offsetY
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
        
        return X,Y
    except Exception as e:
        raise e


def get_reg_dpi():
    dpi = 1
    try:
        platform_name = platform.platform()
        __logger.debug('platform:'+str(platform_name))
        if 'Windows-7' in platform_name :
            return dpi
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop\WindowMetrics") 
        i = 0
        while 1:
            name, value, type = winreg.EnumValue(key, i)
            if('AppliedDPI' in repr(name)):
                dpi = value
                dpi = dpi/96
                break 
            i += 1
    except Exception as e:
        print(e)    
    finally:
        return dpi
 
 
def run_javascript(title="",url="",js="",waitfor=WAIT_FOR,pid=0):
    __logger.debug('run_javascript :['+str(title)+']['+str(url)+']['+str(js)+']')
    text = None
    try:
        print(js)
        param = get_param(title,url,"", "","","","",js,pid)
        starttime = time.time()
        while True:
            __logger.debug(param)
            result=dll.doJionJs(param)
            if result:
                __logger.debug('execute success')
                return True
            else:
                __logger.debug('execute fail')
                return False
    except Exception as e:
        return False
        raise e


def capture_element_img(win_title=None,title=None,url=None,selector=None,in_img_path=None,waitfor=WAIT_FOR):

    try:
        curson_x,curson_y,width,height = get_element_rect(win_title=win_title,title=title,url=url,selector=selector,curson='lefttop',offsetX=0,offsetY=0)

        in_img_path = img.capture_image(win_title=win_title, win_text="", in_img_path=in_img_path,left_indent=curson_x, top_indent=curson_y, width=width, height=height,waitfor=waitfor)

        return in_img_path
    except Exception as e:
        raise e