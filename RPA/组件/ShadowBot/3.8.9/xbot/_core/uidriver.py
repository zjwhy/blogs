from .pipe import PipeClient
from .retry import Retry
from ..errors import UIAError, UIAErrorCode

import uuid
import subprocess
import win32api
import win32con
import win32job
import win32file
import threading
import queue


class _Connection(object):
    def __init__(self):
        self.pipe = PipeClient()
        self.lock = threading.Lock()

    def connect(self, pipeid, timeout):
        for _ in Retry(timeout, error_message='无法连接到UIA'):
            try:
                self.pipe.connect(pipeid)
                break
            except:
                pass

    def execute(self, method, args, timeout=-1):
        if self.pipe is None:
            raise UIAError('UIA尚未初始化', UIAErrorCode.UIDriverConnectionError)
        with self.lock:
            request = {
                'method': method,
                'params': args,
                'options': {
                    'timeout': timeout
                }
            }
            suc = self.pipe.write(request)
            if not suc:
                raise UIAError('发送UIA命令失败, {0}'.format(
                    method), UIAErrorCode.UIDriverConnectionError)
            response = self.pipe.read()
            if response is None:
                raise UIAError(
                    '读取UIA数据失败', UIAErrorCode.UIDriverConnectionError)
            return response


class _Driver(object):
    def __init__(self):
        self.hasinit = False
        # self.hJob = None
        self.connection = _Connection()
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self.consume_async, daemon=True)
        self.thread.start()

    def launch(self, pipe):
        if self.hasinit:
            return
        # pipeid = str(uuid.uuid1())
        # # create driver process with win job object
        # hJob = win32job.CreateJobObject(None, "")
        # extended_info = win32job.QueryInformationJobObject(
        #     hJob, win32job.JobObjectExtendedLimitInformation)
        # extended_info['BasicLimitInformation']['LimitFlags'] = win32job.JOB_OBJECT_LIMIT_BREAKAWAY_OK | win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        # win32job.SetInformationJobObject(
        #     hJob, win32job.JobObjectExtendedLimitInformation, extended_info)
        # child = subprocess.Popen(
        #     [filepath, '--pipe={0}'.format(pipeid)])
        # perms = win32con.PROCESS_TERMINATE | win32con.PROCESS_SET_QUOTA
        # hProcess = win32api.OpenProcess(perms, False, child.pid)
        # win32job.AssignProcessToJobObject(hJob, hProcess)
        # self.hJob = hJob
        # connect pipe
        self.connection.connect(pipe, 10)
        self.hasinit = True

    def execute(self, method, args):
        resp = self.connection.execute(method, args)
        if resp['code'] == 200:
            result = resp['result']
            content = result['content']
            error = result['error']
            if error is None:
                return content
            else:
                raise UIAError(error['message'], UIAErrorCode(error['code']))
        else:
            error_message = 'UIA执行失败, {0}, {1}'.format(
                resp['code'], resp['status'])
            raise UIAError(error_message, UIAErrorCode.UIDriverConnectionError)

    def execute_async(self, method, args):
        self.queue.put((method, args))

    def consume_async(self):
        while True:
            method, args = self.queue.get()
            self.execute(method, args)


_driver = _Driver()


def launch(pipe):
    _driver.launch(pipe)


def execute(method, args=None):
    return _driver.execute(method, args)


def execute_async(method, args):
    _driver.execute_async(method, args)
