'''
win32窗口自动化模块
'''


from .element import Win32Element, SAPElement, _win32_elements_cache
from .._core import uidriver
from .._core.retry import Retry
from .._core.validation import valid, valid_multi, ValidPattern
from ..selector import Selector, TableSelector, _get_selector_by_name
from ..errors import UIAError, UIAErrorCode

from abc import ABCMeta, abstractmethod
from typing import NoReturn, Any, List
import time


class Win32Window(object):
    def __init__(self, controller, hWnd):
        self._controller = controller
        self.hWnd = hWnd

    def get_detail(self, operation) -> str:
        '''
        获取窗口信息
        * @param operation, 获取窗口信息, 如标题
            * `'title'`, 窗口标题
            * `'text'`, 窗口内容
            * `'process_name'`, 窗口进程名
        * @return `str`, 返回窗口信息
        '''

        valid('获取窗口选项', operation, ValidPattern.NotEmpty)
        return self._invoke("GetDetail", {'operation': operation})

    #Activates (gives focus to) a window.
    def activate(self) -> NoReturn:
        '''
        激活窗口
        '''

        self._invoke("Activate")

    def set_state(self, flag) -> NoReturn:
        '''
        设置窗口状态
        * @param flag, 窗口的状态, 如最大化、最小化
            * `'hide'`, 隐藏
            * `'show'`, 显示
            * `'minimize'`, 最小化
            * `'maximize'`, 最大化
            * `'restore'`, 还原
        '''

        valid('设置窗口状态', flag, ValidPattern.NotEmpty)
        if flag == 'hide':
            int_flag = 0
        elif flag == 'show':
            int_flag = 1
        elif flag == 'minimize':
            int_flag = 2
        elif flag == 'maximize':
            int_flag = 3
        elif flag == 'restore':
            int_flag = 4
        else:
            raise ValueError(f"无效的检测内容类型{flag}")

        return self._invoke("SetState", {'flag': int_flag})

    def move(self, *, x=0, y=0) -> NoReturn:
        '''
        将窗口移动到指定位置
        * @param x, 指定位置的横坐标
        * @param y, 指定位置的纵坐标
        '''

        valid('横坐标x', x, (ValidPattern.Type, int))
        valid('纵坐标y', y, (ValidPattern.Type, int))
        self._invoke('Move', {'x': x, 'y': y})

    def resize(self, *, width=1, height=1) -> NoReturn:
        '''
        设置窗口大小
        * @param width, 窗口宽度
        * @param height, 窗口高度
        '''

        valid('宽width', width, (ValidPattern.Min, 0))
        valid('高height', height, (ValidPattern.Min, 0))
        self._invoke("SetSize", {'width': width, 'height': height})

    def close(self) -> NoReturn:
        '''
        关闭窗口
        '''

        self._invoke("Close")

    def is_active(self) -> bool:
        '''
        判断窗口是否是选中(激活)状态
        * @return `bool`, 返回当前窗口的选中状态, 选中返回`True`, 未选中返回`False`
        '''

        return self._invoke('IsActive')

    def wait_active(self, timeout=20) -> NoReturn:
        '''
        等待窗口选中(激活)
        * @param timeout, 等待窗口选中的超时时间, 默认等待事件20s, 超过该时间目标窗口还未被选中则抛出`'UIAError'`异常
        '''

        valid_multi('timeout', timeout, [(ValidPattern.Type, int),
                                         (ValidPattern.Min, -1)])
        for _ in Retry(timeout, interval=0.5, error_message='等待窗体激活超时'):
            if self.is_active():
                break

    def wait_close(self, timeout=20) -> bool:
        '''
        等待窗口关闭
        * @param timeout, 等待窗口关闭的超时时间, 如果超过该时间窗口还未关闭则返回 `False`
            * 等于 0, 不等待
            * 大于 0, 按时间等待
            * 等于 -1, 一直等待
        * @return `bool`, 返回窗口是否关闭的结果, 消失返回 `True`, 否则返回 `False`
        '''

        if timeout == 0:
            return self._invoke("WaitClose", {'timeout': 1})

        for _ in Retry(timeout, interval=0.5, ignore_exception=True):
            if self._invoke("WaitClose", {'timeout': 1}):
                return True
        return False
        

    def find_all(self, selector, *, timeout=20) -> List[Win32Element]:
        '''
        获取窗口中与选择器匹配的全部元素并返回元素列表
        * @param selector, 要查找的选择器, 支持以下格式: 
            * 选择器名称, `str`类型
            * 选择器对象, `Selector`类型
        * @param timeout, 获取窗口相似元素列表超时时间, 默认超时时间为20s
        * @return `List[Win32Element]`, 返回窗口中与目标元素相似的元素列表 
        '''

        _win32_elements_cache.release()
        if isinstance(selector, str):
            selector = _get_selector_by_name(selector)

        if not isinstance(selector, Selector):
            raise ValueError('selector参数类型不正确')
        for _ in Retry(timeout, interval=0.5, ignore_exception=True):
            try:
                element_id_list = self._invoke('QuerySelectorAll',
                                               {'selector': selector.value})
                if len(element_id_list) == 0:
                    continue
                return [self._create_element(eid) for eid in element_id_list]
            except UIAError as e:
                if e.code == UIAErrorCode.PageIsLoading or e.code == UIAErrorCode.NoSuchWindow or e.code == UIAErrorCode.NoSuchElement:
                    pass
                else:
                    raise e
        return []

    def find(self, selector, *, timeout=20) -> Win32Element:
        '''
        获取窗口中与元素选择器匹配的元素, 如果找到多个或者未找到相似的元素则抛出 `UIAError` 异常
         * @param selector, 要查找的选择器, 支持以下格式: 
            * 选择器名称, `str`类型
            * 选择器对象, `Selector`类型
        * @param timeout, 获取窗口相似元素超时时间, 默认超时时间为20s
        * @return `Win32Element`, 返回窗口中与目标元素相似的第一个元素
        '''
        if isinstance(selector, str):
            selector = _get_selector_by_name(selector)

        elements = self.find_all(selector, timeout=timeout)
        if len(elements) == 0:
            raise UIAError('未找到控件', UIAErrorCode.NoSuchElement)
        elif len(elements) > 1:
            raise UIAError('匹配到多个控件, 无法唯一定位', UIAErrorCode.Common)
        else:
            return elements[0]

    def wait_appear(self, selector_or_element, timeout=20) -> bool:
        '''
        等待元素出现
        * @param selector_or_element, 要等待的目标元素, 支持以下格式: 
            * 选择器名称, `str`类型
            * 选择器对象, `Selector`类型
            * Win32元素对象, `Win32Element`类型
        * @param timeout, 在窗口中等待目标元素出现的超时时间, 默认时间是20s
        * @return `bool`, 如果目标元素在窗口中出现了则返回`True`, 否则返回`False`
        '''
        if isinstance(selector_or_element, str):
            selector_or_element = _get_selector_by_name(selector_or_element)

        if isinstance(selector_or_element, Selector):
            for _ in Retry(timeout, interval=0.5, ignore_exception=True):
                try:
                    element_count = self._invoke(
                        'GetElementCount',
                        {'selector': selector_or_element.value})
                    if element_count == 0:
                        continue
                    else:
                        return True
                except UIAError as e:
                    if e.code == UIAErrorCode.PageIsLoading or e.code == UIAErrorCode.NoSuchWindow \
                            or e.code == UIAErrorCode.NoSuchElement or e.code == UIAErrorCode.NoSuchElementID:
                        pass
                    else:
                        break
            return False
        elif isinstance(selector_or_element,
                        Win32Element):  #win32元素的用户级可见性 似乎等同于 元素在树中能否找到节点
            return True
        else:
            raise ValueError('selector_or_element参数类型不正确')

    def wait_disappear(self, selector_or_element, timeout=20) -> bool:
        '''
        等待元素消失
        * @param selector_or_element, 要等待的目标元素, 支持以下格式: 
            * 选择器名称, `str`类型
            * 选择器对象, `Selector`类型
            * Win32元素对象, `Win32Element`类型
        * @param timeout, 在窗口中等待目标元素消失的超时时间, 默认时间是20s
        * @return `bool`, 如果目标元素在窗口中消失了则返回`True`, 否则返回`False`
        '''
        if isinstance(selector_or_element, str):
            selector_or_element = _get_selector_by_name(selector_or_element)

        if isinstance(selector_or_element, Selector):
            for _ in Retry(timeout, interval=0.5, ignore_exception=True):
                try:
                    element_count = self._invoke(
                        'GetElementCount',
                        {'selector': selector_or_element.value})
                    if element_count == 0:
                        return True
                    else:
                        continue
                except UIAError as e:
                    if e.code == UIAErrorCode.PageIsLoading or e.code == UIAErrorCode.NoSuchWindow \
                            or e.code == UIAErrorCode.NoSuchElement or e.code == UIAErrorCode.NoSuchElementID:
                        pass
                    else:
                        break
            return False
        elif isinstance(
                selector_or_element, Win32Element
        ):  #如果只给id的话，就没办法通过查找树来确定其是否消失，只能简单地查一下缓存看是否存在，涉及到缓存更新的问题
            return False
        else:
            raise ValueError('selector_or_element参数类型不正确')

    def contains_element(self, selector) -> bool:
        '''
        当前窗口中是否包含与元素选择器匹配的元素
        * @param selector, 要查找的选择器, 支持以下格式: 
            * 选择器名称, `str`类型
            * 选择器对象, `Selector`类型
        * @return `bool`, 如果窗口包含目标元素则返回`True`, 否则返回`False`
        '''
        if isinstance(selector, str):
            selector = _get_selector_by_name(selector)

        if not isinstance(selector, Selector):
            raise ValueError('selector参数类型不正确')
        try:
            element_count = self._invoke('GetElementCount',
                                         {'selector': selector.value})
            if element_count == 0:
                return False
            else:
                return True
        except UIAError as e:
            if e.code == UIAErrorCode.PageIsLoading or e.code == UIAErrorCode.NoSuchWindow \
                    or e.code == UIAErrorCode.NoSuchElement or e.code == UIAErrorCode.NoSuchElementID:
                return False
            else:
                raise e
        

    def wait_focus(self, timeout=20) -> bool:
        '''
        等待窗口获取焦点
        * @param timeout, 等待窗口获取焦点的超时时间, 默认是20s, 如果超过该时间窗口还未获取焦点则返回 `False`
            * 等于 0, 不等待
            * 大于 0, 按时间等待
            * 等于 -1, 一直等待
        * @return `bool`, 返回窗口是否获取焦点的结果, 获取到焦点返回 `True`, 否则返回 `False`
        '''

        if timeout == 0:
            return self.is_active()

        for _ in Retry(timeout,  interval=0.5, ignore_exception=True):
            if self.is_active():
                return True
        return False

    def wait_focusout(self, timeout=20) -> bool:
        '''
        等待窗口失去焦点
        * @param timeout, 等待窗口失去焦点的超时时间, 默认是20s, 如果超过该时间窗口还未失去焦点则返回 `False`
            * 等于 0, 不等待
            * 大于 0, 按时间等待
            * 等于 -1, 一直等待
        * @return `bool`, 返回窗口是否失去焦点的结果, 失去焦点返回 `True`, 否则返回 `False`
        '''

        if timeout == 0:
            return not self.is_active()

        for _ in Retry(timeout, interval=0.5, ignore_exception=True):
            if not self.is_active():
                return True
        return False



    def _create_element(self, eid) -> Win32Element:
        if eid.startswith('SAP'):
            return SAPElement('Win32Element', eid, self)
        else:
            return Win32Element('Win32Element', eid, self)

    def _invoke(self, action, args=None):
        all_args = {'hWnd': self.hWnd}
        if args is not None:
            all_args.update(args)
        return uidriver.execute(f'{self._controller}.{action}', all_args)
