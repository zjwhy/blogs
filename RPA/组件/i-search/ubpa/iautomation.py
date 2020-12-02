# -*- coding: utf-8 -*-
'''
Created on 2018年8月29日

@author: wu.xin
'''
import ctypes
import json
from msilib import Control
import subprocess
import time 
import traceback
from ubpa import iwin
from ubpa.iconstant import WAIT_FOR
from ubpa.ierror import WinNotFoundError
import uiautomation
from uiautomation.uiautomation import ControlType

from comtypes import automation
import win32con

import ubpa.encrypt as encrypt
import uiautomation as automation
import ubpa.iimg as img


# from ubpa.ierror import WinNotFoundError
# from ubpa.ilog import ILog
class SelectorParam:
    """表达式中的属性"""
    Selector = "selector"
    Win = "win"
    ControlType = "ControlTypeID"
    ControlTypeName = "ControlType"
    Index = "Index"
    Name= "Name"
    Aid = "aid"
 
# __logger = ILog(__file__)

WinSearchDepth = 2
    
def get_element_rectangle(win_class=None,win_name=None,selector=None,waitfor=WAIT_FOR):
    '''
    返回 :(left, top, right, bottom)
    '''
    try:
        automation.SetGlobalSearchTimeOut(waitfor)
        if win_name!=None:
            iwin.do_win_activate(win_title=win_name, waitfor=waitfor)
        
        ctrl = get_control(win_class, win_name, selector)
        
        return ctrl.BoundingRectangle()
    except Exception as e:
        raise e   
        
def do_moveto(win_class=None,win_name=None,selector=None,curson='center',offsetX=0,offsetY=0,waitfor=WAIT_FOR):
    try:
        automation.SetGlobalSearchTimeOut(waitfor)
        if win_name!=None:
            iwin.do_win_activate(win_title=win_name, waitfor=waitfor)
            
#         win = get_win_control(win_class, win_name)
#         win.SwitchToThisWindow()
#         win.SetFocus()
        
        ctrl = get_control(win_class, win_name, selector)
        
        ratioX,ratioY = get_pos_ratio(curson,offsetX,offsetY)        
        
        ctrl.MoveCursor(ratioX, ratioY)
    except Exception as e:
        raise e

def get_text(win_class=None,win_name=None,selector=None,return_field='value',waitfor=WAIT_FOR):
    try:
        automation.SetGlobalSearchTimeOut(waitfor)
        ctrl = get_control(win_class, win_name, selector)
        
        ctrl = automation.Control.CreateControlFromControl(ctrl)
        if return_field == 'value':
            return ctrl.AccessibleCurrentValue() 
        else:
            return ctrl.AccessibleCurrentName() 
    except Exception as e:
        raise e


def set_text(win_class=None,win_name=None,selector=None,text=None,waitfor=WAIT_FOR):
    try:
        text = encrypt.decrypt(text)
        automation.SetGlobalSearchTimeOut(waitfor) 
        if win_name!=None:
            iwin.do_win_activate(win_title=win_name, waitfor=waitfor)
        
        ctrl = get_control(win_class, win_name, selector)
        
        ctrl = automation.Control.CreateControlFromControl(ctrl)
        ctrl.SetValue(text)
    except Exception as e:
        raise e

def do_check(win_class=None,win_name=None,selector=None,action="check",waitfor=WAIT_FOR):
    try:
        automation.SetGlobalSearchTimeOut(waitfor) 
        if win_name!=None:
            iwin.do_win_activate(win_title=win_name, waitfor=waitfor)
        
        ctrl = get_control(win_class, win_name, selector)
        
        ctrl = automation.Control.CreateControlFromControl(ctrl)
        
        state = ctrl.CurrentToggleState()
        
        if action == "check":
            if state == 0 :
                return ctrl.Toggle()
        else:
            if state == 1 :
                return ctrl.Toggle()
    except Exception as e:
        raise e
    
    
def get_check_status(win_class=None,win_name=None,selector=None,waitfor=WAIT_FOR):
    '''
    获取CheckBox的状态    0:未选中，1:选中
    '''    
    try:
        automation.SetGlobalSearchTimeOut(waitfor) 
        if win_name!=None:
            iwin.do_win_activate(win_title=win_name, waitfor=waitfor)
        
        ctrl = get_control(win_class, win_name, selector)
        
        ctrl = automation.Control.CreateControlFromControl(ctrl)
        return ctrl.CurrentToggleState()
    except Exception as e:
        raise e

def get_selected_item(win_class=None,win_name=None,selector=None,waitfor=WAIT_FOR):
    try:
        automation.SetGlobalSearchTimeOut(waitfor) 
        if win_name!=None:
            iwin.do_win_activate(win_title=win_name, waitfor=waitfor)
        
        
        ctrl = get_control(win_class, win_name, selector)
        
        ctrl = automation.Control.CreateControlFromControl(ctrl)
        return ctrl.CurrentValue() 
    except Exception as e:
        raise e


def get_selecte_items(win_class=None,win_name=None,selector=None,waitfor=WAIT_FOR):
    pass 
        
def do_selecte_item(win_class=None,win_name=None,selector=None,select_string=None,waitfor=WAIT_FOR):  
    try:
        automation.SetGlobalSearchTimeOut(waitfor) 
        if win_name!=None:
            iwin.do_win_activate(win_title=win_name, waitfor=waitfor)
        
        ctrl = get_control(win_class, win_name, selector)
        
        ctrl = automation.Control.CreateControlFromControl(ctrl)
        ctrl.Select(select_string)
    except Exception as e:
        raise e      

def do_click_element(win_class=None,win_name=None,selector=None,waitfor=WAIT_FOR):
    '''
    do mouse click backgroud
    '''
    ctrl = None
    try:
        automation.SetGlobalSearchTimeOut(waitfor) 
        if win_name!=None:
            iwin.do_win_activate(win_title=win_name, waitfor=waitfor)
            
        ctrl = get_control(win_class, win_name, selector) 
        ctrl = automation.Control.CreateControlFromControl(ctrl)
        ctrl.SetFocus()
        do_click_element_msg(ctrl)
        if ctrl.IsInvokePatternAvailable() :
            ctrl.Invoke()
             
    except Exception as e:
        print(e)
        do_click_element_msg(ctrl)
#         raise e
    
    
     
def do_click_element_msg(control): 
    lparam = control.Handle
    automation.Win32API.PostMessage(lparam, 0x0201, 1, 0)
    automation.Win32API.PostMessage(lparam, 0x0202, 1, 0)
    
     
   
    
    
def do_click(win_class=None,win_name=None,selector=None,button='left',curson='center',offsetX=0,offsetY=0,times=1,waitfor=WAIT_FOR,run_mode='unctrl'):
    '''
    点击控件
    win_class:窗口的ClassName
    win_name:窗口的Name
    selector:控件的信息
    button:left,right,middle
    curson:center,lefttop,rightbottom
    offsetX:Click(10, 10): click left+10, top+10
    offsetY:Click(-10, -10): click right-10, bottom-10
    times:1单击，2双击 
    '''
# #     __logger.debug('automation 点击控件:[' + str(win_name) + '][' + str(control) + ']')
    try:
        automation.SetGlobalSearchTimeOut(waitfor)
        if run_mode == 'ctrl':
           return do_click_element(win_class=win_class,win_name=win_name,selector=selector) 
        
        if win_name!=None:
            iwin.do_win_activate(win_title=win_name, waitfor=waitfor)
        
        ctrl = get_control(win_class, win_name, selector) 
         
        if run_mode == 'unctrl':
            ratioX,ratioY = get_pos_ratio(curson,offsetX,offsetY) 
            #ctrl.SetFocus()
            if button == 'left' :
                if times == 1:
                    ctrl.Click(ratioX, ratioY)                                        
                else:
                    ctrl.DoubleClick(ratioX, ratioY)
            elif button == 'right':
                ctrl.RightClick(ratioX, ratioY)
            elif button == 'middle':
                ctrl.MiddleClick(ratioX, ratioY)  
        
    except Exception as e:
        raise e
    
    
def get_pos_ratio(curson='center',offsetX=0,offsetY=0): 
    
    #如果是小数的话，则以百分比来算
    if isinstance(offsetX, float) and isinstance(offsetX, float):        
        ratioX = offsetX
        ratioY = offsetY   
    else:
        ratioX = round(offsetX)
        ratioY = round(offsetY)
        
    if curson == 'center':
        ratioX = 0.5
        ratioY = 0.5    
    elif curson == 'lefttop' : #左上
        ratioX = offsetX
        ratioY = offsetY
    elif curson == 'rightbottom':
        if offsetX == 0 :
            ratioX = -1
        else:
            ratioX = 0 - offsetX
            
        if offsetY == 0 :   
            ratioY = -1
        else:
            ratioY = 0 - offsetY
    return ratioX,ratioY           
 


def get_control(win_class=None,win_name=None,selector=None):
    try:
        win = get_win_control(win_class, win_name)
        dics = selector[SelectorParam.Selector]
        if len(dics) == 1 :    #如果只有一选项，而且只有名字
            name =  None
            control_type = None
            index = 1
            dic = dics[0]
            if ( SelectorParam.Name in dic.keys() ):
                name = dic[SelectorParam.Name] 
                
            if (SelectorParam.ControlType in dic.keys()):
                control_type = int(dic[SelectorParam.ControlType],16)
                
            if (SelectorParam.Index in dic.keys()):
                index = int(dic[SelectorParam.Index])
            if name != None and control_type == None:
                #print("直接按照名字查找")
                ctrl = get_control_by_name(win,name,index) 
            else:
                ctrl = get_last_control(win, selector) 
        else:
            ctrl = get_last_control(win, selector) 
        return ctrl
    except Exception as e:
        raise e 





def get_win_control(win_class=None,win_name=None):
    try:
        if win_class!=None and win_name!=None: 
            wind = automation.Control(ClassName=win_class,SubName = win_name,searchDepth=WinSearchDepth)
        elif win_class!=None and win_name==None: 
            wind = automation.Control(ClassName=win_class,searchDepth=WinSearchDepth)
        elif win_class==None and win_name!=None: 
            wind = automation.Control(SubName = win_name,searchDepth=WinSearchDepth)  
        if(wind.Exists(5) != True):
            raise WinNotFoundError() 
        return wind
    except Exception as e:
        raise e
    
    
def get_last_control(win_control,dics):
    try:
        s_dics = dics[SelectorParam.Selector]
        dic_len = len(s_dics)
        idx = dic_len-1
        ctrl = win_control
        while idx >= 0:
            dic = s_dics[idx]
            idx-=1  
            ctrl = get_one_control(ctrl,dic)
        
        return ctrl 
    except Exception as e:
        raise e  

 
def get_one_control(control,dic):  
    try: 
        #print(dic)
        name =  None
        control_type = None
        index = 1
        
        if ( SelectorParam.Name in dic.keys() ):
            name = dic[SelectorParam.Name] 
            
        if (SelectorParam.ControlType in dic.keys()):
            control_type = int(dic[SelectorParam.ControlType],16)
            
        if (SelectorParam.Index in dic.keys()):
            index = int(dic[SelectorParam.Index])
        
        if name != None and control_type != None :
            ctrl = automation.Control(searchFromControl= control,SubName = name,ControlType=control_type,foundIndex=index,searchDepth=1)
        elif name != None and control_type == None :
            ctrl = automation.Control(searchFromControl= control,SubName=name,foundIndex=index,searchDepth=1)
        elif name == None and control_type != None :    
            ctrl = automation.Control(searchFromControl= control,ControlType=control_type,foundIndex=index,searchDepth=1)
        else:
            raise Exception('ui parameter cannot be all null')
             
       # print(ctrl.AutomationId,ctrl.ControlTypeName,ctrl.Exists(),ctrl.Name)
        return ctrl        
    except Exception as e:
        raise e       
        
        
        
def get_control_by_name(control,name,foundIndex=1):
    try:
        ctrl = automation.Control(searchFromControl= control,SubName=name,foundIndex=foundIndex) 
        return ctrl
    except Exception as e:
        raise e


def GetWindowLong(handle, nIndex):
    """Call API GetWindowLong from user32.dll"""
    return ctypes.windll.user32.GetWindowLongW(handle, nIndex)


   
def do_get_pos(left=None, top=None, width=None, height=None, curson='center',offsetX=0, offsetY=0):
    curson_x = None
    curson_y = None
    curs = str(curson).lower()

    try:
        if curs == "center":
            curson_x = left + width / 2 + offsetX
            curson_y = top + height / 2 + offsetY
        if curs == "lefttop":
            curson_x = left + offsetX
            curson_y = top + offsetY
        if curs == "righttop":
            curson_x = left + width + offsetX
            curson_y = top + offsetY
        if curs == "leftbottom":
            curson_x = left + offsetX
            curson_y = top + height + offsetY
        if curs == "rightbottom":
            curson_x = left + width + offsetX
            curson_y = top + height + offsetY
        return curson_x, curson_y
    except Exception as e:
        raise e

def get_element_rect(win_class=None, win_name=None, selector=None,curson='lefttop',offsetX=0,offsetY=0, waitfor=WAIT_FOR):
    '''
    返回 :(curson_x, curson_y, width, height)
    '''
    try:
        automation.SetGlobalSearchTimeOut(waitfor)
        # if win_name != None:
        #     iwin.do_win_activate(win_title=win_name, waitfor=waitfor)

        ctrl = get_control(win_class, win_name, selector)
        result = ctrl.BoundingRectangle

        left = result[0]
        top = result[1]
        width = result[2] - result[0]
        height = result[3] - result[1]

        if curson != None and curson != "":

            curson_x, curson_y = do_get_pos(left, top, width, height, curson=curson, offsetX=offsetX, offsetY=offsetY)
            return curson_x, curson_y, width, height
        else:
            return left,top,width,height

    except Exception as e:
        raise e


def capture_element_img(win_class=None, win_name=None, selector=None,in_img_path=None, waitfor=WAIT_FOR):
    try:
        curson_x, curson_y, width, height = get_element_rect(win_class=win_class, win_name=win_name, selector=selector,curson='lefttop')

        in_img_path = img.capture_image(win_title=win_name, win_text='', in_img_path=in_img_path,left_indent=curson_x, top_indent=curson_y, width=width, height=height,waitfor=waitfor)
        return in_img_path
    except Exception as e:
        raise e
