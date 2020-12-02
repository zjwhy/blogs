# -*- coding: utf-8 -*-
import os
import random
import string
import time
from ubpa.ierror import Au3ExecError
from ubpa.ilog import ILog
from ubpa.iresult import IResult

import ubpa.base_native_ait as nit



__logger = ILog(__file__)

'''
title     标题 
text      提示输入数据的类型, 意义.
default   [可选] 输入框初始显示的默认值.
password  [可选] 替换所有输入字符的显示字符. 默认为空("")或设置第一个字符为空格, 使输入字符原样显示.
width     [可选] 窗口宽度.
heidht    [可选] 窗口高度.
left      [可选] 输入框的左边距离. default(默认) = 居中显示.
Top       [可选] 输入框的上边距离. default(默认) = 居中显示.
timeout   [可选] 输入框自动关闭的延迟时间(秒).
'''

# 组装脚本
def ibox_pack_au3(title,text,default,password,width,height,left,Top,timeout): 
    intput = "#include <MsgBoxConstants.au3>" \
          + '\n' + "#PRE_Change2CUI=y" \
          + '\n' + "$R_VALUE = 0" \
          + '\n' + "$R_VALUE = InputBox('InputBox','"  +  str(text) + "',"   +  "'" +str(default) +"','" +str(password) +"',"+str(width)+","+str(height) +",Default,Default)"\
          + '\n' + "ConsoleWrite($R_VALUE)" 
    return intput

# 组装脚本
def msgbox_pack_au3(box_mode,msg,title,timeout):
    msg = "#include <MsgBoxConstants.au3>" \
          + '\n' + "#PRE_Change2CUI=y" \
          + '\n' + "$R_VALUE = 0" \
          + '\n' + "$R_VALUE = MsgBox("+str(box_mode)+",'"+str(msg)+"' ,'"+str(title)+"', "+str(timeout)+" )"\
          + '\n' + "ConsoleWrite($R_VALUE)" \

    return msg


#数据输入对话框
def input_box(text='请输入',default='',password='',width=0,height=150,timeout=0):
    '''
    text:输入提示语
    default:默认值
    password:密码替代符
    width:宽
    height:高
    timeout:超时
    '''
    __logger.echo_msg(u"Ready to execute[input_box]")
    title='输入框',
    left='Default'
    top='Default',
    au3_content = ibox_pack_au3(title, text, default, password, width, height, left, top,timeout)  ##组装生成au3所需的数据,组装au3文件内容
    try:
        tmp_au3_file_path = nit.gen_au3_file(au3_content)  # 生成XXX.au3文件并返回路径
        status, error_string, stdout_string = nit.run_autoit(tmp_au3_file_path)
        if status:
            '''程序执行错误'''
            raise Au3ExecError('input_box excute fail')
        time.sleep(2)
        result = str(nit.get_cmd_message1(stdout_string)) 
        
    except Exception as e:
        raise e
    finally:
        nit.cleanup(tmp_au3_file_path)
        __logger.echo_msg(u"End operation")
        return result

#消息对话框
def msg_box(title="INFO", msg="", timeout=0): 
    '''
    title:标题
    msg:内容
    timeout:超时    
    '''
    __logger.echo_msg(u"Ready to execute[msg_box]")
    box_mode=0 
    au3_content = msgbox_pack_au3(box_mode, title, msg, timeout)  ##组装生成au3所需的数据,组装au3文件内容
    try:
        tmp_au3_file_path = nit.gen_au3_file(au3_content)  # 生成XXX.au3文件并返回路径
        status, error_string, stdout_string = nit.run_autoit(tmp_au3_file_path)
        if status:
            '''程序执行错误'''
            raise Au3ExecError('msg_box excute fail')
        return True
    except Exception as e:
        raise e
    finally:
        nit.cleanup(tmp_au3_file_path)
        __logger.echo_msg(u"End operation")

