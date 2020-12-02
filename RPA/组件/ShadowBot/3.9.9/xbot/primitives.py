'''
公用数据模块
'''

import os
from ._core import _sdmodules
from xbot.win32 import clipboard

class VariableDict(dict):
    def __init__(self, keys=None):
        dict.__init__(self)
        if keys is not None:
            for key in keys:
                dict.__setitem__(self, key, None)

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            raise KeyError(f'找不到名称为{key}的全局变量')



class ResourceReader():
    def __init__(self, loader, app_folder):
        self._base = os.path.join(app_folder, 'resources')
        self._loader = loader
    
    def get_text(self, filename, encoding='utf-8') -> str:
        '''
        获取资源文件的文本内容
        * @param filename, 资源文件名
        * @param encoding, 读取文件时的编码格式, 默认是以 `'utf-8'` 的格式读取
        * @return `str`, 返回资源文件的文本内容
        '''

        data = self.get_bytes(filename)
        return data.decode(encoding)

    def get_bytes(self, filename) -> bytes:
        '''
        获取资源文件的二进制信息
        * @param filename, 资源文件名
        * @return `bytes`, 返回资源文件的二进制信息
        '''

        filepath = os.path.join(self._base, filename)
        return self._loader.get_data(filepath)

    def copy_to(self, filename, dest_filename):
        '''
        将资源文件的内容拷贝到目标文件中
        * @param filename, 资源文件名
        * @param dest_filename, 资源文件的内容需要拷贝到的文件的绝对路径, 如 'D:\\123.txt'
        '''

        data = self.get_bytes(filename)
        dir_path = os.path.split(dest_filename)[0]
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(dest_filename, 'wb') as f:
            f.write(data)

    def copy_to_clipboard(self, filenames):
        '''
        将资源文件添加到剪切板
        * filenames, 资源文件名列表, 如['123.txt', '234.xml']
        '''

        if filenames is None or len(filenames) == 0:
            raise ValueError("资源文件名列表不能为空")
        
        clipboard.set_file([os.path.join(self._base, file) for file in filenames])