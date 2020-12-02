#-*- coding:utf-8 -*-#
'''
Created on 2018年9月6日

@author: ibm
'''
import json
import time
from urllib import request
from ubpa.iconstant import WAIT_FOR
from ubpa.ilog import ILog
import threading
__logger = ILog(__file__)


def send_http(json_data, host, port=6004, add_pr='',try_times=2, waitfor=WAIT_FOR):
    count = 0
    while True:
        try:
            url = host + ':' + str(port) + add_pr
            data = json.dumps(json_data).encode(encoding='utf-8')
            header_dict = {"Content-Type": "application/json"}
            req = request.Request(url=url, data=data, headers=header_dict)
            res = request.urlopen(req, timeout=waitfor)
            break
        except Exception as e:
                print(e)
                count += 1
                if count >= try_times:
                    __logger.debug(r'[send_http_json] exceute fail')
                    break
                __logger.debug(r'[send_http_json] exceute fail,waite for excute next time')
                time.sleep(1)


def send_http_json(json_data, host, port=6004, add_pr = '', try_times=2, waitfor=WAIT_FOR):
    '''
    json_data:发送的json数据 非字符串
    host:地址
    port:http端口
    try_times:重试次数
    waitfor:等待超时
    '''
    __logger.debug(r'ready for excute [send_http_json]')
    try:
        t = threading.Thread(target=send_http(json_data, host, port, add_pr,try_times, waitfor),
                             name='send_http_json_thread')
        t.start()
        t.join(WAIT_FOR)
    except Exception as e:
        raise e
    finally:
        __logger.debug(r'finish excute [send_http_json]')



