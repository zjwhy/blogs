import ctypes
import threading
import time

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

def thread_routine():
    while True:
        ctypes.windll.kernel32.SetThreadExecutionState(
            ES_CONTINUOUS | \
            ES_SYSTEM_REQUIRED | \
            ES_DISPLAY_REQUIRED)
        time.sleep(30)

def start_prevent_os_sleep():
    thread = threading.Thread(target = thread_routine, daemon = True)
    thread.start()