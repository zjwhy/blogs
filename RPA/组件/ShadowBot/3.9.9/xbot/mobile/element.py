from .._core import uidriver
from typing import NoReturn, Any, List
from .._core.validation import valid, valid_multi, ValidPattern

import time

class MobileElement(object):
    def __init__(self, controller, sid, eid):
        self._controller = controller
        self.sid = sid
        self.eid = eid
    
    def __del__(self):
        _mobile_elements_cache.append(self.eid)
    
    def click(self, *, delay_after=1) -> NoReturn:
        '''
        单击手机元素
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        '''
        self._invoke('Click')
        if delay_after > 0:
            time.sleep(delay_after)
    
    def dblclick(self, *, delay_after=1) -> NoReturn:
        '''
        双击手机元素
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        '''
        self._invoke('DblClick')
        if delay_after > 0:
            time.sleep(delay_after)
    
    def longpress(self, *, delay_after=1) -> NoReturn:
        '''
        长按手机元素
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        '''
        self._invoke('LongPress')
        if delay_after > 0:
            time.sleep(delay_after)
    
    def input(self, text: str, *, append=False, delay_after=1) -> NoReturn:
        '''
        填写手机输入框
        * @param text, 需要填写到手机输入框中的文本内容
        * @param append, 是否追加输入, 追加输入会保留输入框中原有内容, 在原有内容最后面追加写入内容，非追加时写入会覆盖输入框中原有内容, 默认值为`False`, 非追加写入
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        '''
        self._invoke('Input', {
                                'text': text,
                                'append': append
                              }
                    )
        if delay_after > 0:
            time.sleep(delay_after)
    
    def get_text(self) -> str:
        '''
        获取元素的文本内容
        * @return `str`, 元素的文本内容
        '''
        return self._invoke('GetText')
    
    def get_attribute(self, name: str) -> str:
        '''
        获取手机元素的属性值
        * @param name, 元素的属性名
        * @return `str`, 元素的属性值
        '''
        return self._invoke('GetAttribute', {'name': name})
    
    def screenshot(self, folder_path, *, filename=None) -> NoReturn:
        '''
        对手机元素进行截图并保存
        * @param folder_path, 截图保存的路径
        * @param filename, 截图保存时的文件名, 可为空, 为空时会更具当前时间自动生成文件名
        '''
        valid('保存文件夹', folder_path, ValidPattern.NotEmpty)
        self._invoke('Screenshot', { 'folderPath': folder_path, 'fileName': filename })
    
    def get_bounding(self) -> tuple:
        '''
        获取手机元素在手机屏幕中的位置
        * @return `tuple`, 返回元素的位置信息, 如('x', 'y', 'width', 'height')
        '''
        bounding = self._invoke('GetBounding')
        return (bounding['x'], bounding['y'], bounding['width'], bounding['height'])

    def _invoke(self, action, args=None):
        all_args = {'sessionId': self.sid, 'elementId': self.eid}
        if args is not None:
            all_args.update(args)
        return uidriver.execute(f'{self._controller}.{action}', all_args)
    
# 管理待释放的元素列表，延迟释放（时机为下一次find_elements）
class _MobileElementCache(object):
    def __init__(self):
        self._list = list()

    def append(self, item):
        self._list.append(item)

    def release(self):
        if len(self._list) > 0:
            element_ids = self._list.copy()
            self._list.clear()
            uidriver.execute(f'Mobile.ReleaseElementCache',
                             {'elementIds': element_ids})


_mobile_elements_cache = _MobileElementCache()