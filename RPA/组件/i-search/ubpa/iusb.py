# -*- coding: utf-8 -*-
'''
Created on 2018.9.1

@author: ibm
'''
#!/usr/bin/python3
import serial
from serial.tools.list_ports import comports
from serial.tools import hexlify_codec
from time import sleep
import threading
import json
from ubpa.ilog import ILog
__logger = ILog(__file__)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
global receive_flag
receive_flag = True 

def ask_for_port():
    """\
    Show a list of ports and ask the user for a choice. To make selection
    easier on systems with long device names, also allow the input of an
    index.
    """
    print('\n--- Available ports:\n')
    ports = []
    for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
        print('--- {:2}: {:20} {!r}\n'.format(n, port, desc))
        ports.append(port)
    return ports


def command_set (default_port=None, command_buf = ""):

    ser = serial.Serial(default_port,115200, timeout=0.5)
    if ser.isOpen():
        print("open success")
        out_date = bytes.fromhex(command_buf)
        ser.write(out_date)
        """loop and copy serial->console"""
        n = 0
        num = 0
        text = ""
        buf = ""
        global receive_flag
        receive_flag = True
        timer = threading.Timer(5, func)
        timer.start()
        while receive_flag:
            # read all that is there or wait for one byte
            buf = ser.read(ser.in_waiting or 1)
            if buf:
                num = len(buf)
                n += num
                text += buf.decode()
                buf = ''
            if "}}" in text:
                receive_flag = False
                timer.cancel()
                return text
        else:
            sleep(0.1)
            ser.close()
    else:
        print("open failed")


def func():
    global receive_flag
    receive_flag = False
    print("receive failed")


def get_com_index(dcode):
    __logger.echo_msg(u"Ready to execute[get_com_index]")
    finally_COM_list = ask_for_port()
    data = 'A5 5A ' + str(dcode).zfill(2) + ' 30 00 00 FF'
    for com_port in finally_COM_list:
        result = command_set(default_port=com_port, command_buf=data)
        if len(result) != 0:
            __logger.echo_msg(u"[get_com_index] end execute")
            return com_port


def convert_radix(dcode=1, port_idx=1):
    '''
    对板号 和 usb端口号 进行 进制转换
    '''
    if dcode <= 9:
        dcode = str(dcode).zfill(2)
    elif dcode >= 10:
        dcode = hex(dcode)
        dcode = dcode[2:].zfill(2)

    port_idx -= 1
    if port_idx <= 9:
        port_idx = str(port_idx).zfill(2)
    elif port_idx >= 10:
        port_idx = hex(port_idx)
        port_idx = port_idx[2:].zfill(2)
    return dcode, port_idx


def port_power_off_only(dcode=1, port_idx=1):
    '''
    只关闭USBHUB某一个usb口，打开其余的usb口
        dcode: usbhub 板号
        port_idx: usb端口号
    '''
    __logger.echo_msg(u"Ready to execute[port_power_off_only]")
    #data = 'A5 5A 01(板号) 00 01[端口] 00 FF'
    try:
        com_port = get_com_index(dcode)
        dcode, port_idx = convert_radix(dcode, port_idx)
        data = 'A5 5A ' + dcode + ' 20 00 00 FF'
        command_set(default_port=com_port, command_buf=data)

        data = 'A5 5A ' + dcode + ' 00 ' + port_idx + ' 00 FF'
        result = command_set(default_port=com_port, command_buf=data)
        if result != None:
            result = True
        else:
            result = False
        return result
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"[port_power_off_only] end execute")


def port_power_on_only(dcode=1, port_idx=1):
    '''
    只开启USBHUB某个usb口，关闭其余的usb口
        dcode:     usbhub 板号
        port_idx: usb端口号
    '''
    __logger.echo_msg(u"Ready to execute[port_power_on_only]")
    # data = 'A5 5A 01(板号) 00 01[端口] 01 FF'
    try:
        com_port = get_com_index(dcode)
        dcode, port_idx = convert_radix(dcode, port_idx)
        data = 'A5 5A ' + dcode + ' 10 00 00 FF'
        command_set(default_port=com_port, command_buf=data)

        data = 'A5 5A ' + dcode + ' 00 ' + port_idx + ' 01 FF'
        result = command_set(default_port=com_port, command_buf=data)
        if result != None:
            result = True
        else:
            result = False
        return result
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"[port_power_on_only] end execute")


def port_power_off(dcode=1, port_idx=1):
    '''
    关闭USBHUB某个usb口
        dcode:      usbhub 板号
        port_idx:   usb端口号
    '''
    __logger.echo_msg(u"Ready to execute[port_power_off]")
    try:
        com_port = get_com_index(dcode)
        dcode, port_idx = convert_radix(dcode,port_idx)
        # data = 'A5 5A 01 00 00 00 FF'
        data = 'A5 5A ' + dcode + ' 00 ' + port_idx + ' 00 FF'
        result = command_set(default_port=com_port, command_buf=data)
        if result != None:
            result = True
        else:
            result = False
        return result
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"[port_power_off] end execute")


def port_power_on(dcode=1, port_idx=1):
    '''
    打开USBHUB某个usb口
        dcode:      usbhub 板号
        port_idx:   usb端口号
    '''
    __logger.echo_msg(u"Ready to execute[port_power_on]")
    try:
        com_port = get_com_index(dcode)
        dcode, port_idx = convert_radix(dcode, port_idx)
        # data = 'A5 5A 01 00 00 00 FF'
        data = 'A5 5A ' + dcode + ' 00 ' + port_idx + ' 01 FF'
        result = command_set(default_port=com_port, command_buf=data)
        print(result)
        if result != None:
            result = True
        else:
            result = False
        return result
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"[port_power_on] end execute")


def port_power_status(dcode=1, port_idx=1):
    '''
    查询USBHUB某个usb口状态
        com_port: COM口号
        dcode:    usbhub 板号
        port_idx: usb端口号
    '''
    __logger.echo_msg(u"Ready to execute[port_power_status]")
    # data = 'A5 5A 01 30 00 00 FF'
    try:
        com_port = get_com_index(dcode)
        dcode, port_idx2= convert_radix(dcode, port_idx)
        data = 'A5 5A ' + dcode + ' 30 '+ port_idx2 + ' 00 FF'
        result = command_set(default_port=com_port, command_buf=data)
        json_result = json.loads(result)
        port_name = 'U'+ str(port_idx)
        port_power_status = json_result['status'][port_name]
        return port_power_status
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"[port_power_status] end execute")


def port_power_status_all(dcode=1):
    '''
    查询USBHUB全部usb口状态
        dcode: usbhub 板号
    '''
    __logger.echo_msg(u"Ready to execute[port_power_status_all]")
    # data = 'A5 5A 01 30 00 00 FF'
    try:
        com_port = get_com_index(dcode)
        dcode= convert_radix(dcode)
        data = 'A5 5A ' + dcode[0] + ' 30 00 00 FF'
        result = command_set(default_port=com_port, command_buf=data)
        json_result = json.loads(result)
        port_power_status = json_result['status']
        return port_power_status
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"[port_power_status_all] end execute")


