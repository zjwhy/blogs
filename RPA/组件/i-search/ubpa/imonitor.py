# -*- coding: utf-8 -*-
'''


@author: ibm
'''
from _socket import AF_INET, SOCK_DGRAM
import _thread
from ctypes import cdll

import json
import socket
from socketserver import BaseRequestHandler, UDPServer
import sys
import threading
import time
from ubpa import iautomation, ics, ijava, iie, ichrome_firefox

import mouse
from mouse._mouse_event import ButtonEvent
#import pyHook
import pythoncom
import win32api
from win32gui import IsWindow, IsWindowEnabled, IsWindowVisible, GetWindowText, EnumWindows, GetActiveWindow, GetFocus
import win32gui
from ubpa.iconstant import *

from ubpa.ilog import ILog



class AppType:
    """This class defines the values of type"""
    AppUia = 'uia'
    AppIe = 'ie'
    AppJava = 'java'
    AppChrome = 'chrome'
    AppFirefox = 'firefox'
    
class IEventMonitorThread(threading.Thread): 
    
    def __init__(self,appType="java",title=None,element_json={},processer=None,repeat=True):
        threading.Thread.__init__(self)
        monitor = IEventMonitor(appType="java",title=None,element_json={},processer=None,repeat=True)
        self.monitor = monitor 
        
    def run(self):
        print ("开始线程：" + self.name) 
        print ("退出线程：" + self.name)
        while True:
            print(11)
            time.sleep(1)
     
            
# thread1 = IEventMonitorThread(1, "Thread-1", 1)
# thread1.start()
# while True:
#     print(22)
#     time.sleep(2)
            
class IEventMonitor():
     
    
    def __init__(self,appType=None,title=None,element_json={},processer=None,repeat=True):
        self.appType = appType
        self.title = title
        self.element_json = element_json   #字典
        self.repeat = repeat
        # print("-"*20)
        # print(processer)
        self.processer = processer
        self.status = 'working'  #正在 获取元素
    
        self.prev_position = (0,0)
        self.lasttime = 0
        self.scal = self.getScale()
        self.listening = True
    
    def onMonitor(self):
        try:
            mouse._listener.add_handler(self.onEvents)
            mouse._listener.listen() 
        except Exception as e:
            print(e)
    
    
    
    
    def onEvents(self,event):
        try:
            if self.listening : 
                w = win32gui.GetForegroundWindow()
                title = win32gui.GetWindowText(w)
                if self.title == None or (self.title !=None and self.title in title):
    
                    current_time = time.time()
                    if isinstance(event, ButtonEvent) and event.event_type=='up':
                        interval_time = current_time - self.lasttime
                        if interval_time < 1:
                            pass
                        elif self.prev_position == mouse.get_position():
                            pass
                        else:
                            self.prev_position = mouse.get_position()
                            emement_pos = self.getElementRect()
                            if self.processer == None :
                                raise Exception('event processer is none')
        #                     print('emement_pos:',emement_pos)
        #                     print('mouse click pos',self.prev_position[0]*self.scal,self.prev_position[1]*self.scal)
                            self.lasttime = current_time
                            if self.isInRect(self.prev_position, emement_pos):
                                self.processer()
                                if self.repeat!=True:
                                    self.listening = False
#                                     mouse._listener.stop_listen(self) 

#                     
        except Exception as e:
            raise e
         
    
    
    def isInRect(self,mpos,rect):
        if mpos!=None and rect!=None:
            x_range = (rect[0],rect[0]+rect[2])
            y_range = (rect[1],rect[1]+rect[3])
            # x = mpos[0]*self.scal
            # y = mpos[1]*self.scal

            x = mpos[0]
            y = mpos[1]

            if x>x_range[0] and x<x_range[1] and y>y_range[0] and y<y_range[1]:
#                 print("点击范围内")
                return True
            else:
#                 print("点击范围外")
                return False
        else:
            return False  
    
    
    def getScale(self):   
        scal_dll = cdll.LoadLibrary("../../bin/ScreenScaling.dll")
        sc = scal_dll.GetScreenScaling()
        print('scaling:',sc)
        return sc/100


    def addProcesser(self,processer):
        self.processer = processer 
    
    
    def getElementRect(self):
        pos = None
        try:
            self.status = 'working'
            pjson_dic = self.element_json

            if self.appType == AppType.AppJava:
                java_program = pjson_dic["program"]
                java_title = pjson_dic["title"]
                java_className = pjson_dic["className"]
                java_selector = pjson_dic["selector"]

                pos = ijava.get_element_rect(program=java_program, title=java_title, className=java_className, selector=java_selector)
            if self.appType == AppType.AppIe:
                ie_win_title = pjson_dic["win_title"]
                ie_url = pjson_dic["url"]
                ie_selector = pjson_dic["selector"]

                pos = iie.get_element_rect(win_title=ie_win_title, url=ie_url, selector=ie_selector)
            if self.appType == AppType.AppUia:
                uia_win_class = pjson_dic["win_class"]
                uia_win_name = pjson_dic["win_name"]
                uia_selector = pjson_dic["selector"]

                pos = iautomation.get_element_rect(win_class=uia_win_class, win_name=uia_win_name, selector=uia_selector)
            if self.appType == AppType.AppChrome:
                chrome_attrMap = pjson_dic["attrMap"]
                chrome_index = pjson_dic["index"]
                chrome_tagName= pjson_dic["tagName"]
                chrome_title = pjson_dic["title"]
                chrome_url = pjson_dic["url"]

                pos = ichrome_firefox.get_element_rect_chrome(attrMap=chrome_attrMap, index=chrome_index, tagName=chrome_tagName, title=chrome_title, url=chrome_url)
            if self.appType == AppType.AppFirefox:
                firefox_attrMap = pjson_dic["attrMap"]
                firefox_index = pjson_dic["index"]
                firefox_tagName = pjson_dic["tagName"]
                firefox_title = pjson_dic["title"]
                firefox_url = pjson_dic["url"]

                pos = ichrome_firefox.get_element_rect_firefox(attrMap=firefox_attrMap, index=firefox_index, tagName=firefox_tagName, title=firefox_title, url=firefox_url)
            else:
                pass
            
                
        except Exception as e:
            print(e)
        finally:
            self.status = 'unworking'
            return pos


    


    def start_monitor(self):
        self.onMonitor()


    def start_monitor_thread(self):
        t = threading.Thread(target=self.onMonitor)
        t.daemon = True #主线程运行结束时不对这个子线程进行检查而直接退出，子线程将随主线程一起结束，而不论是否运行完成。
        t.start()
 
#     _thread.start_new_thread(monitor.onMonitor()) 
#     print(111)   
    
logger = ILog(__file__)

dll = cdll.LoadLibrary("../../bin/RpaCommon.dll")

def trigger_tags(tag):
    ''' 发送服务器TAG 日志 '''
    logger.debug("Start sending TAG LOG")
    try:
        result = dll.sendTagJson(tag)
        if result != 0:
            logger.debug("Successfully send TAG LOG")
            return True
        else:
            logger.debug("failed send TAG LOG")
            return False
    except Exception as e:
        raise e


def trigger_tips(level='INFO',msg=''):
    ''' 发送助手弹框信息 '''
    logger.debug("Start sending ASIST MSG")
    try:
        result = dll.sendHelpInfo(level, msg)
        if result != 0:
            logger.debug("Successfully send ASIST MSG")
            return True
        else:
            logger.debug("failed send ASIST MSG")
            return False
    except Exception as e:
        raise e


def trigger_procs(proc_name, proc_code, proc_path, proc_parm='', mode='hand'):
    ''' 发送助手机器人操作 '''
    logger.debug("Start sending ASIST ROBOT")
    try:
        result = dll.sendHelpAi(proc_name, proc_code, proc_path, proc_parm, mode)
        if result != 0:
            logger.debug("Successfully send ASIST ROBOT")
            return True
        else:
            logger.debug("failed send ASIST ROBOT")
            return False
    except Exception as e:
        raise e


    

# element_json={
# 	"program": "javaw.exe",
# 	"title": "SOAPClient",
# 	"className": "SunAwtFrame",
# 	"selector": [{
# 		"headerCol": "",
# 		"headerRow": "",
# 		"nIndex": 0,
# 		"name": "Set Servers",
# 		"role": "push button",
# 		"state": "",
# 		"tableCol": -1,
# 		"tableRow": -1,
# 		"virtName": "Set Servers"
# 	}]
# }
#

# def abc():
#     print("abc")
# _element_json = {"selector":{"selector":[{"ControlType":"编辑","ControlTypeID":"0xC354","Index":"1"}]},"win_class":"Notepad","win_name":"无标题 - 记事本"}
# monitor=IEventMonitor(appType="uia",title=r'无标题 - 记事本',element_json=_element_json,processer=abc,repeat=False)
# monitor.start_monitor()
        
# monitor = IEventMonitor(appType="java", title='SOAPClient', element_json=element_json, processer=abc, repeat=True)
# # monitor.addProcesser(abc)
# start_monitor_thread(monitor)
#
#
#
#
# while True:
#     print(1)
#     time.sleep(5)





# monitor.onMonitor()


# thread.start_new_thread ( function, args[, kwargs] )


# while True:
#     print(1111)
#     time.sleep(1)

#循环获取消息 

# 
# def on_move(x, y):
#     print('Pointer moved to {0}'.format(
#         (x, y)))
#  s


# selector = {"selector":[{"ControlType":"窗格","ControlTypeID":"0xC371","Index":"1"},{"ControlType":"窗格","ControlTypeID":"0xC371","Index":"2"},{"ControlType":"窗格","ControlTypeID":"0xC371","Index":"1"},{"ControlType":"窗格","ControlTypeID":"0xC371","Index":"1"},{"ControlType":"窗口","ControlTypeID":"0xC370","Index":"1"},{"ControlType":"窗格","ControlTypeID":"0xC371","Index":"3"}]}
# selectorJson = {"selector":[{"ControlType":"窗格","ControlTypeID":"0xC371","Index":"1"},{"ControlType":"窗格","ControlTypeID":"0xC371","Index":"2"},{"ControlType":"窗格","ControlTypeID":"0xC371","Index":"1"},{"ControlType":"窗格","ControlTypeID":"0xC371","Index":"1"},{"ControlType":"窗口","ControlTypeID":"0xC370","Index":"1"},{"ControlType":"窗格","ControlTypeID":"0xC371","Index":"3"}]}
# pos = iautomation.get_element_rect(win_class=r'TForm1',win_name=r'TCP/UDP Socket 调试工具 V2.3 - [数据收发窗口]',selector=selectorJson,waitfor=0)
# print(pos)


# pos = ijava.get_element_rect(program=r'java.exe',title=r'SOAPClient',className=r'SunAwtFrame',selector=[{"headerCol":"","headerRow":"","nIndex":0,"name":"Set Servers","role":"push button","state":"","tableCol":-1,"tableRow":-1,"virtName":"Set Servers"}],waitfor=0)
# print(pos)
# motriger = IEventMonitor("java","title",selector,repeat) 
# motriger.addProcesser(triger_33333333333)
# motriger.doMonitor()


# d = False
# prev_position = None
# lasttime = time.time()
#  
# w = win32gui.GetForegroundWindow()
# title = win32gui.GetWindowText(w)
# print(title)
# def callback(event):
#     from ubpa import iautomation
#     if isinstance(event, ButtonEvent) and event.event_type=='up' :  
#         global prev_position,lasttime
#         current_time = time.time()
#         interval_time = current_time - lasttime
#         print(interval_time)
#         if interval_time < 1 :
#             print('按键间隔小于1秒，不处理')
#         elif prev_position == mouse.get_position():
#             print('与上次位置相同，不做处理')
#         else:
#             prev_position = mouse.get_position() 
#             try:
#                 pos = ijava.get_element_rect(program=r'java.exe',title=r'SOAPClient',className=r'SunAwtFrame',selector=[{"headerCol":"","headerRow":"","nIndex":0,"name":"Set Servers","role":"push button","state":"","tableCol":-1,"tableRow":-1,"virtName":"Set Servers"}],waitfor=0)
#                 print(pos)
#             except Exception as e:
#                 print(e)
#             print('mouse pos',prev_position[0]*1.25,prev_position[1]*1.25) 
#         lasttime = current_time
#          
# 
# mouse._listener.add_handler(callback)
# mouse._listener.listen()

# def on_click(x, y, button, pressed):
#     print('{0} at {1}'.format(
#         'Pressed' if pressed else 'Released',
#         (x, y)))
#     if not pressed:
#         # Stop listener
#         return False


    
    
# def get_event():
#     time.sleep(1)   
#     return 0,1,2,3
# 
# while True :
#     p = get_event()
#     print(p)    
    
    
# class TimeHandler(BaseRequestHandler):
#     def handle(self):
#         print('Got connection from', self.client_address)
#         # Get message and client socket
#         msg, sock = self.request
#         print(msg)
#         resp = time.ctime()
#         sock.sendto(resp.encode('ascii'), self.client_address)
# 
# 
# serv = UDPServer(('', 9999), TimeHandler)
# serv.serve_forever()
#     
      
# a= 'ddd'  
# def tt(**kwargs):
#     print('ttt')
#     print(kwargs['p1'])  
# eve = IEventMonitor()
# eve.addProcess(tt,p1='abc')
# eve.onEvents()        