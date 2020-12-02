from .pipe import PipeClient
from .retry import Retry
from ..errors import UIAError, UIAErrorCode

import time
import threading

_pipe = PipeClient()
_lock = threading.Lock()


def connect(pipeid):
    for _ in Retry(5, error_message='无法连接到Robot'):
        try:
            _pipe.connect(pipeid)
            break
        except:
            pass


def execute(method, args):
    while True:
        resp = _send_request(method, args)
        if resp['code'] == 200:
            result = resp['result']
            content = result['content']
            error = result['error']
            if error is None:
                return content
            else:
                raise Exception(error['message'])
        elif resp['code'] == 100:  # promise
            method = 'ResolvePromise'
            args = {'promiseId': resp['result']['content']}
            time.sleep(0.4)
            continue
        else:
            error_message = 'Robot执行命令失败, {0}, {1}'.format(
                resp['code'], resp['status'])
            raise Exception(error_message)


def _send_request(method, args, timeout=-1):
    with _lock:
        request = {
            'method': method,
            'params': args,
            'options': {
                'timeout': timeout
            }
        }
        suc = _pipe.write(request)
        if not suc:
            raise Exception(f'发送Robot命令失败, {method}')
        response = _pipe.read()
        if response is None:
            raise Exception('无法读取Robot返回内容')
        return response
