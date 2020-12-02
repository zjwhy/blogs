import win32file
import json
import struct


class PipeClient(object):

    def __init__(self):
        self.handle = None

    def connect(self, pipe_name):
        pipe_path = r'\\.\pipe\{0}'.format(pipe_name)
        self.handle = win32file.CreateFile(pipe_path,
                                           win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                                           win32file.FILE_SHARE_WRITE, None,
                                           win32file.OPEN_EXISTING, 0, None)

    def write(self, obj):
        content = json.dumps(obj)
        content_bytes = content.encode('utf-8')
        suc = self._write_data(struct.pack('i', len(content_bytes)))
        if not suc:
            return False
        suc = self._write_data(content_bytes)
        if not suc:
            return False
        return True

    def read(self):
        size_bytes = self._read_data(4)
        if size_bytes is None:
            return None
        size, = struct.unpack('i', size_bytes)
        content_bytes = self._read_data(size)
        if content_bytes is None:
            return None
        content = content_bytes.decode('utf-8')
        return json.loads(content)

    def _read_data(self, size):
        try:
            code, data = win32file.ReadFile(self.handle, size)
            if(code == 0):
                return data
            else:
                return None
        except:
            return None

    def _write_data(self, data):
        try:
            code, _ = win32file.WriteFile(self.handle, data)
            if(code == 0):
                return True
            else:
                return False
        except:
            return False

    def close(self):
        try:
            win32file.CloseHandle(self.handle)
        except:
            pass
