# -*- coding: utf-8 -*-

from ..errors import UIAError, UIAErrorCode

import time


class Retry():
    def __init__(self, timeout=-1, times=-1, *, interval=0.2, error_message=None, ignore_exception=False):
        self._timeout = timeout
        self._times = times
        self._interval = interval
        self._error_message = error_message or '操作超时'
        self._ignore_exception = ignore_exception

    def __iter__(self):
        return _RetryIterator(self._timeout, self._times, self._interval, self._error_message, self._ignore_exception)


class _RetryIterator():
    def __init__(self, timeout, times, interval, error_message, ignore_exception):
        self._timeout = timeout
        self._times = times
        self._interval = interval
        self._error_message = error_message
        self._ignore_exception = ignore_exception
        self._index = 0
        self._starttime = time.time()

    def __iter__(self):
        return self

    def __next__(self):
        if(self._index > 0):
            time.sleep(self._interval)
            if (self._times >= 0 and self._index > self._times) or \
                    (self._timeout >= 0 and time.time()-self._starttime > self._timeout):
                if self._ignore_exception or self._timeout == 0 or self._times == 0:
                    raise StopIteration()
                else:
                    raise UIAError(self._error_message, UIAErrorCode.Timeout)
        retrytime = self._index
        self._index += 1
        return retrytime
