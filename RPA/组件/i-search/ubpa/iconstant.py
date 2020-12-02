# -*- coding:utf-8 -*-
'''
Created on 2018-3-26

@author: Wu.Xin
常量定义
'''
import os

''' 
全局waitfor 时长为5秒
'''
WAIT_FOR = 5


'''
全局图片等待 时长10秒
'''
WAIT_FOR_IMG = 10


'''
全局日志是否输出控制台
'''
LOG_TO_CONSOLE = True


'''
错误尝试间隔 ; 默认1
'''
TRY_INTERVAL = 1
    
'''
临时文件夹
'''
TEMP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..\..\..\.."))+ os.sep+'temp'+ os.sep
#TEMP_PATH = 'd:/temp/'
#print(TEMP_PATH)   

