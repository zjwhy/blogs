from __future__ import annotations
from .._core import uidriver
from .._core.retry import Retry
from .._core.validation import valid, valid_multi, ValidPattern
from ..selector import Selector, _get_selector_by_name
from ..errors import UIAError, UIAErrorCode
from xbot.app import logging

import abc
import typing
import time


class WebElement(metaclass=abc.ABCMeta):
    '''
    网页元素自动化模块
    '''

    def __init__(self, controller, bid, eid):
        self._controller = controller
        self.bid = bid
        self.eid = eid

    def find(self, selector, *, timeout=10) -> WebElement:
        '''
        在当前元素中获取与选择器匹配的网页元素对象, 如果找到多个或者未找到相似控件则抛出 `UIAError` 异常
        * @param selector, 要查找的选择器, 支持以下格式: 
            * 选择器名称, `str`类型
            * 选择器对象, `Selector`类型
        * @param timeout, 查找并返回与当前选择器匹配网页元素的元素对象, 默认超时时间20s
        * @return `WebElement`, 返回与目标元素相似的第一个网页元素对象
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

    def find_by_css(self, css_selector, *, timeout=10) -> WebElement:
        '''
        在当前元素中获取符合CSS选择器的网页元素, 如果找到多个或者未找到相似控件则抛出 `UIAError` 异常
        * @param css_selector, CSS选择器 (`str`)
        * @param timeout, 查找并返回当前网页满足CSS选择器的网页元素对象, 默认超时时间20s
        * @return `WebElement`, 返回满足CSS选择器条件的第一个网页元素对象
        '''

        elements = self.find_all_by_css(css_selector, timeout=timeout)
        if len(elements) == 0:
            raise UIAError('未找到控件', UIAErrorCode.NoSuchElement)
        elif len(elements) > 1:
            raise UIAError('匹配到多个控件, 无法唯一定位', UIAErrorCode.Common)
        else:
            return elements[0]

    def find_by_xpath(self, xpath_selector, *, timeout=10) -> WebElement:
        '''
        在当前元素中获取符合xpath选择器的网页元素, 如果找到多个或者未找到相似控件则抛出 `UIAError` 异常
        * @param xpath_selector, xpath选择器 (`str`)
        * @param timeout, 查找并返回当前网页满足Xpath选择器的网页元素对象, 默认超时时间20s
        * @return `WebElement`, 返回满足Xpath选择器条件的第一个网页元素对象
        '''

        elements = self.find_all_by_xpath(xpath_selector, timeout=timeout)
        if len(elements) == 0:
            raise UIAError('未找到控件', UIAErrorCode.NoSuchElement)
        elif len(elements) > 1:
            raise UIAError('匹配到多个控件, 无法唯一定位', UIAErrorCode.Common)
        else:
            return elements[0]

    def find_all(self, selector, *, timeout=10) -> list[WebElement]:
        '''
        在当前元素中获取与选择器匹配的相似网页元素列表
        * @param selector, 要查找的选择器, 支持以下格式: 
            * 选择器名称, `str`类型
            * 选择器对象, `Selector`类型
        * @param timeout, 查找并返回与当前选择器匹配的全部网页元素列表的超时时间, 默认超时时间20s
        * @return `list<WebElement>`, 返回与目标网页元素相似的全部网页元素列表
        '''
        if isinstance(selector, str):
            selector = _get_selector_by_name(selector)

        if not isinstance(selector, Selector):
            raise ValueError('selector参数类型不正确')
        for _ in Retry(timeout, interval=0.5, ignore_exception=True):
            try:
                eid_list = self._invoke('QuerySelectorAll', {
                                        'selector': selector.value})
                if len(eid_list) == 0:
                    continue
                return [self._create_element(self.bid, x) for x in eid_list]
            except UIAError as e:
                if e.code == UIAErrorCode.NoSuchWindow or e.code == UIAErrorCode.NoSuchElement or UIAErrorCode.NoSuchElementID:
                    pass
                else:
                    raise e
        return []

    def find_all_by_css(self, css_selector, *, timeout=10) -> list[WebElement]:
        '''
        在当前元素中获取符合CSS选择器的网页元素列表
        * @param css_selector, CSS选择器 (`str`)
        * @param timeout, 查找并返回满足CSS选择器条件的全部网页元素列表的超时时间, 默认超时时间20s
        * @return `list<WebElement>`, 返回满足CSS选择器条件的全部网页元素列表
        '''

        for _ in Retry(timeout, interval=0.5, ignore_exception=True):
            try:
                eid_list = self._invoke('QueryCSSSelectorAll', {
                                        'cssSelector': css_selector})
                if len(eid_list) == 0:
                    continue
                return [self._create_element(self.bid, x) for x in eid_list]
            except UIAError as e:
                if e.code == UIAErrorCode.NoSuchWindow or e.code == UIAErrorCode.NoSuchElement or UIAErrorCode.NoSuchElementID:
                    pass
                else:
                    raise e
        return []

    def find_all_by_xpath(self, xpath_selector, *, timeout=10) -> list[WebElement]:
        '''
        在当前元素中获取符合Xpath选择器的网页元素列表
        * @param xpath_selector, Xpath选择器 (`str`)
        * @param timeout, 查找并返回满足Xpath选择器条件的全部网页元素列表的超时时间, 默认超时时间20s
        * @return `list<WebElement>`, 返回满足Xpath选择器条件的全部网页元素列表
        '''

        for _ in Retry(timeout, interval=0.5, ignore_exception=True):
            try:
                eid_list = self._invoke('QueryXPathSelectorAll', {
                                        'xpathSelector': xpath_selector})
                if len(eid_list) == 0:
                    continue
                return [self._create_element(self.bid, x) for x in eid_list]
            except UIAError as e:
                if e.code == UIAErrorCode.NoSuchWindow or e.code == UIAErrorCode.NoSuchElement or UIAErrorCode.NoSuchElementID:
                    pass
                else:
                    raise e
        return []

    def parent(self) -> WebElement:
        '''
        获取当前元素的父元素
        * @return `WebElement`, 返回当前元素的父元素
        '''

        eid = self._invoke('Parent')
        return None if eid is None else self._create_element(self.bid, eid)

    def children(self) -> list[WebElement]:
        '''
        获取当前元素的所有子元素
        * @return `List<WebElement>`, 返回当前元素的所有子元素
        '''

        eid_list = self._invoke('Children')
        return [self._create_element(self.bid, x) for x in eid_list]

    def child_at(self, index) -> WebElement:
        '''
        获取指定位置的子元素
        * @param index, 子元素的位置索引，从0开始计数
        * @return `WebElement`, 返回指定位置的子元素
        '''

        eid = self._invoke('ChildAt', {'index': index})
        return None if eid is None else self._create_element(self.bid, eid)

    def next_sibling(self) -> WebElement:
        '''
        获取下一个并列的兄弟元素
        * @return `WebElement`, 返回下一个并列的兄弟元素
        '''

        eid = self._invoke('NextSibling')
        return None if eid is None else self._create_element(self.bid, eid)

    def click(self, *, button='left', simulative=True, keys='none', delay_after=1, anchor=None) -> typing.NoReturn:
        '''
        单击当前网页元素
        * @param button, 点击时的具体鼠标按键, 如鼠标左键、右键等, 默认是左键
            * `'left'`, 鼠标左键
            * `'right'`, 鼠标右键
        * @param simulative, 是否模拟人工点击, 模拟人工时鼠标回有明显的移动轨迹移动到目标元素上再进行点击, 不模拟时会瞬间移动到目标元素上并进行点击, 默认值为`True`
        * @param keys, 单击网页元素时的键盘辅助按钮, 如`Alt`键、`Ctrl`键等, 可以为空默认值为空
            * `'none'`, 不需要键盘辅助按钮
            * `'alt'`, 使用alt键作为辅助按钮
            * `'ctrl'`, 使用ctrl键作为辅助按钮
            * `'shift'`, 使用shift键作为辅助按钮
            * `'win'`, 使用win(窗口)键作为辅助按钮
        * @param anchor, 锚点, 鼠标点击元素的位置以及偏移量元组, 可为 `None`, 默认值为 `None` 为 `None` 时默认点击目标中心且无偏移量, 参数结构如下:
            * `'sudoku_part'`, 鼠标点击的位置, 默认点击中心
                * `'topLeft'`, 点击左上角
                * `'topCenter'`, 点击上中部
                * `'topRight'`, 点击右上角
                * `'middleLeft'`, 点击左中部
                * `'middleCenter'`, 点击中心
                * `'middleRight'`, 点击中部
                * `'bottomLeft'`, 点击下角
                * `'bottomCenter'`, 点击下中部
                * `'bottomRight'`, 点击右下角
                * `'random'`, 随机在元素矩形范围内选择锚点
            * `'offset_x'`, 鼠标位置的水平偏移量
            * `'offset_y'`, 鼠标位置的垂直偏移量
        * @param delay_after, 执行成功后延迟执行时间, 默认时间为1s
        '''
        sudoku_part, offset_x, offset_y = (
            'middleCenter', 0, 0) if anchor is None else anchor
        self._invoke('Click', {'button': button,
                               'simulative': simulative,
                               'keys': keys,
                               'sudokuPart': sudoku_part,
                               'offsetX': offset_x,
                               'offsetY': offset_y})
        if delay_after > 0:
            time.sleep(delay_after)

    def dblclick(self, *, simulative=True, delay_after=1, anchor=None) -> typing.NoReturn:
        '''
        双击当前网页元素
        * @param simulative, 是否模拟人工双击, 模拟人工时鼠标回有明显的移动轨迹移动到目标元素上再进行双击, 不模拟时会瞬间移动到目标元素上并进行双击, 默认值为`True`
        * @param delay_after, 执行成功后延迟执行时间, 默认时间为1s
        * @param anchor, 锚点, 鼠标双击元素的位置以及偏移量元组, 可为 `None`, 默认值为 `None` 为 `None` 时默认双击目标中心且无偏移量, 参数结构如下:
            * `'sudoku_part'`, 鼠标双击的位置, 默认双击中心
                * `'topLeft'`, 双击左上角
                * `'topCenter'`, 双击上中部
                * `'topRight'`, 双击右上角
                * `'middleLeft'`, 双击左中部
                * `'middleCenter'`, 双击中心
                * `'middleRight'`, 双击中部
                * `'bottomLeft'`, 双击下角
                * `'bottomCenter'`, 双击下中部
                * `'bottomRight'`, 双击右下角
                * `'random'`, 随机在元素矩形范围内选择锚点
            * `'offset_x'`, 鼠标位置的水平偏移量
            * `'offset_y'`, 鼠标位置的垂直偏移量
        '''
        sudoku_part, offset_x, offset_y = (
            'middleCenter', 0, 0) if anchor is None else anchor
        self._invoke('DblClick', {'simulative': simulative,
                                  'sudokuPart': sudoku_part,
                                  'offsetX': offset_x,
                                  'offsetY': offset_y})
        if delay_after > 0:
            time.sleep(delay_after)

    def input(self, text: str, *, simulative=True, append=False, contains_hotkey=False, force_ime_ENG=False, send_key_delay=50, focus_timeout=1000, delay_after=1, anchor=None) -> typing.NoReturn:
        '''
        填写网页输入框
        * @param text, 需要填写到网页输入框元素中的文本内容, 可包含快捷键
        * @param simulative, 模拟输入: 通过模拟人工的方式触发输入事件; 非模拟输入(自动化接口输入): 调用元素自身实现的自动化接口输入; 默认值为`True`
        * @param append, 是否是追加输入, 追加输入时不会覆盖输入框中原有的内容, 会在原有内容的末尾追加新的内容, 非追加输入时输入内容会覆盖掉输入框中原有内容, 默认值为`False`
        * @param contains_hotkey, 输入内容是否包含快捷键, 该参数只在模拟人工输入时生效, 默认值为`False`
        * @param force_ime_ENG, 使用模拟输入时会自动切换当前输入法为英文输入状态, 以避免输入法造成的输入错误问题。存在不常见的输入法切换英文输入状态不成功的情况, 需要指定强制加载美式键盘(ENG), 确保模拟输入不受中文输入法影响, 默认值为`False`
        * @param send_key_delay, 两次按键之间的时间间隔(对影刀浏览器该参数无效)，默认为50ms
        * @param focus_timeout, 焦点超时时间(获取焦点和输入操作的间隔), 默认为1000ms
        * @param delay_after, 执行成功后延迟执行时间, 默认时间为1s
        * @param anchor, 锚点, 鼠标点击元素的位置以及偏移量元组, 示例: anchor=('topLeft', 100, 100), 可为 `None`, 默认值为 `None` 为 `None` 时默认点击目标中心且无偏移量, 参数结构如下:
            * `'sudoku_part'`, 鼠标点击的位置, 默认点击中心
                * `'topLeft'`, 点击左上角
                * `'topCenter'`, 点击上中部
                * `'topRight'`, 点击右上角
                * `'middleLeft'`, 点击左中部
                * `'middleCenter'`, 点击中心
                * `'middleRight'`, 点击中部
                * `'bottomLeft'`, 点击下角
                * `'bottomCenter'`, 点击下中部
                * `'bottomRight'`, 点击右下角
                * `'random'`, 随机在元素矩形范围内选择锚点
            * `'offset_x'`, 鼠标位置的水平偏移量
            * `'offset_y'`, 鼠标位置的垂直偏移量
        '''
        # 参数处理
        sudoku_part, offset_x, offset_y = (
            'middleCenter', 0, 0) if anchor is None else anchor
        # 方法调用
        self._invoke('Input', {'text': text,
                               'simulative': simulative,
                               'append': append,
                               'containsHotkey': contains_hotkey,
                               'forceIme2ENG': force_ime_ENG,
                               'sudokuPart': sudoku_part,
                               'offsetX': offset_x,
                               'offsetY': offset_y,
                               "sendKeyDelay": send_key_delay,
                               'focusTimeout': focus_timeout}
                     )
        if delay_after > 0:
            time.sleep(delay_after)

    def clipboard_input(self, text: str, *, append=False, focus_timeout=1000, delay_after=1, anchor=None) -> typing.NoReturn:
        '''
        通过剪切板填写网页输入框(可有效避免输入法问题)
        * @param text, 需要填写到网页输入框元素中的文本内容
        * @param append, 是否是追加输入, 追加输入时不会覆盖输入框中原有的内容, 会在原有内容的末尾追加新的内容, 非追加输入时输入内容会覆盖掉输入框中原有内容, 默认值为`False`
        * @param focus_timeout, 焦点超时时间(获取焦点和输入操作的间隔), 默认为1000ms
        * @param delay_after, 执行成功后延迟执行时间, 默认时间为1s
        * @param anchor, 锚点, 鼠标点击元素的位置以及偏移量元组, 可为 `None`, 默认值为 `None` 为 `None` 时默认点击目标中心且无偏移量, 参数结构如下:
            * `'sudoku_part'`, 鼠标点击的位置, 默认点击中心
                * `'topLeft'`, 点击左上角
                * `'topCenter'`, 点击上中部
                * `'topRight'`, 点击右上角
                * `'middleLeft'`, 点击左中部
                * `'middleCenter'`, 点击中心
                * `'middleRight'`, 点击中部
                * `'bottomLeft'`, 点击下角
                * `'bottomCenter'`, 点击下中部
                * `'bottomRight'`, 点击右下角
                * `'random'`, 随机在元素矩形范围内选择锚点
            * `'offset_x'`, 鼠标位置的水平偏移量
            * `'offset_y'`, 鼠标位置的垂直偏移量
        '''
        sudoku_part, offset_x, offset_y = (
            'middleCenter', 0, 0) if anchor is None else anchor
        self._invoke('ClipboardInput', {'text': text, 'append': append,
                                        'sudokuPart': sudoku_part,
                                        'offsetX': offset_x,
                                        'offsetY': offset_y,
                                        'focusTimeout': focus_timeout}
                     )
        if delay_after > 0:
            time.sleep(delay_after)

    def focus(self) -> typing.NoReturn:
        '''
        选中(激活)当前元素
        '''

        self._invoke('Focus')

    def hover(self, simulative=True, delay_after=1, anchor=None) -> typing.NoReturn:
        '''
        鼠标悬停在当前网页元素上
        * @param simulative, 是否模拟人工悬停, 模拟人工悬停时会有明显的鼠标移动轨迹, 非模拟时鼠标会瞬间移动目标元素上
        * @param delay_after, 执行成功后延迟执行时间, 默认时间为1s
        * @param anchor, 锚点, 鼠标悬停元素的位置以及偏移量元组, 可为 `None`, 默认值为 `None` 为 `None` 时默认点击目标中心且无偏移量, 参数结构如下:
            * `'sudoku_part'`, 鼠标悬停的位置, 默认悬停在中心
                * `'topLeft'`, 悬停在左上角
                * `'topCenter'`, 悬停在上中部
                * `'topRight'`, 悬停在右上角
                * `'middleLeft'`, 悬停在左中部
                * `'middleCenter'`, 悬停在中心
                * `'middleRight'`, 悬停在中部
                * `'bottomLeft'`, 悬停左下角
                * `'bottomCenter'`, 悬停在下中部
                * `'bottomRight'`, 悬停在右下角
                * `'random'`, 随机在元素矩形范围内选择锚点
            * `'offset_x'`, 鼠标位置的水平偏移量
            * `'offset_y'`, 鼠标位置的垂直偏移量
        '''

        sudoku_part, offset_x, offset_y = (
            'middleCenter', 0, 0) if anchor is None else anchor
        self._invoke('Hover', {'simulative': simulative,
                               'sudokuPart': sudoku_part,
                               'offsetX': offset_x,
                               'offsetY': offset_y})
        if delay_after > 0:
            time.sleep(delay_after)

    def get_text(self) -> str:
        '''
        获取当前网页元素的文本内容
        * @return `str`, 返回当前网页元素的文本内容
        '''

        return self._invoke('GetText')

    def get_html(self) -> str:
        '''
        获取当前网页元素的HTML内容
        * @return `str`, 返回当前网页元素的HTNL内容
        '''

        return self._invoke('GetHtml')

    def get_value(self) -> str:
        '''
        获取当前网页元素的值
        * @return `str`, 返回当前网页元素的值
        '''

        return self._invoke('GetValue')

    def set_value(self, value: str) -> typing.NoReturn:
        '''
        设置当前网页元素的文本值
        * @param value, 需要设置到网页元素上的文本值
        '''

        self._invoke('SetValue', {'value': value})

    def check(self, mode='check', delay_after=1) -> typing.NoReturn:
        '''
        设置网页复选框
        * @param mode, 设置网页复选框的结果, 默认为选中
            * `'check'`, 选中复选框
            * `'uncheck'`, 取消选中
            * `'toggle'`, 取反, 如当前是`'check'`则改为`'unchenck'`, 反正则从 `'uncheck'` 变为 `'check'`
         * @param delay_after, 执行成功后延迟执行时间, 默认时间为1s
        '''

        self._invoke('Check', {'mode': mode})
        if delay_after > 0:
            time.sleep(delay_after)

    def select(self, item: str, *, mode='fuzzy', delay_after=1) -> typing.NoReturn:
        '''
        按选项内容设置单选网页下拉框元素
        * @param item, 要设置的网页下拉框元素的某一项的文本内容
        * @param mode, 查找项的匹配模式, 默认是模糊匹配
            * `'fuzzy'`, 模糊匹配
            * `'exact'`, 精准匹配
            * `'regex'`, 正则匹配
        * @param delay_after, 执行成功后延迟执行时间, 默认时间为1s
        '''

        self._invoke('Select', {'item': item, 'mode': mode})
        if delay_after > 0:
            time.sleep(delay_after)

    def select_multiple(self, items: typing.List[str], *, mode='fuzzy', append=False, delay_after=1) -> typing.NoReturn:
        '''
        按选项内容设置多选网页下拉框元素
        * @param item, 要设置的多选网页下拉框元素的某一项或多项的文本内容
        * @param mode, 查找项的匹配模式, 默认是模糊匹配
            * `'fuzzy'`, 模糊匹配
            * `'exact'`, 精准匹配
            * `'regex'`, 正则匹配
        * @param append, 是否追加设置, 默认值为`False`
        * @param delay_after, 执行成功后延迟执行时间, 默认时间为1s
        '''

        self._invoke('SelectMultiple', {
                     'items': items, 'mode': mode, 'append': append})
        if delay_after > 0:
            time.sleep(delay_after)

    def select_by_index(self, index: int, delay_after=1) -> typing.NoReturn:
        '''
        按下标设置单选网页下拉框元素
        * @param index, 要设置的单选网页下拉框元素的某一项下标值, 下标值从`0`开始
        * @param delay_after, 执行成功后延迟执行时间, 默认时间为1s
        '''

        self._invoke('SelectByIndex', {'index': index})
        if delay_after > 0:
            time.sleep(delay_after)

    def select_multiple_by_index(self, indexes: typing.List[int], *, append=False, delay_after=1) -> typing.NoReturn:
        '''
        按下标设置多选网页下拉框元素
        * @param index, 要设置的多项网页下拉框元素的某一项或多项的下标值列表, 下标值从`0`开始
        * @param append, 是否追加设置, 默认值为`False`
        * @param delay_after, 执行成功后延迟执行时间, 默认时间为1s
        '''

        self._invoke('SelectMultipleByIndex', {
                     'indexes': indexes, 'append': append})
        if delay_after > 0:
            time.sleep(delay_after)

    def get_select_options(self) -> typing.List[typing.Tuple]:
        '''
        获取网页下拉框当前选中的值
        * @return `typing.List[typing.Tuple]`, 返回下拉框当前被选中的值的列表，如果是单选下拉框则返回长度为1的列表
        '''

        options = self._invoke('GetSelectOptions')
        return [(x['name'], x['value'], x['selected']) for x in options]

    def get_all_select_items(self) -> typing.List[str]:
        '''
        获取网页下拉框全部下拉选项
        * @return `typing.List[str]`, 返回下拉框的全部下拉选项列表
        '''

        return self._invoke('GetAllSelectItems')

    def get_selected_item(self) -> typing.List[str]:
        '''
        获取网页下拉框当前选中的项
        * @return `typing.List[str]`, 返回下拉框当前选中项
        '''

        return self._invoke('GetSelectedItem')

    def set_attribute(self, name: str, value: str) -> typing.NoReturn:
        '''
        设置网页元素属性值
        * @param name, 元素属性名称
        * param value, 要设置的元素属性值
        '''

        self._invoke('SetAttribute', {'name': name, 'value': value})

    def get_attribute(self, name: str) -> str:
        '''
        获取网页元素属性值
        * @param name, 元素属性名称
        * @return `str`, 返回网页元素目标属性的属性值
        '''

        return self._invoke('GetAttribute', {'name': name})

    def get_all_attributes(self) -> typing.List[typing.Tuple]:
        '''
        获取网页元素的全部属性值
        * @return `typing.List[typing.Tuple]`, 返回目标网页元素的全部属性名与属性值的组合列表
        '''

        attrs = self._invoke('GetAllAttributes')
        return [(x['name'], x['value']) for x in attrs]

    def get_bounding(self, to96dpi=True, relative_to='screen') -> typing.Tuple:
        '''
        获取网页元素相对于屏幕或浏览器客户区左上角的位置
        * @param to96dpi, 是否需要将边框属性转换成dpi为96的对应属性值
        * @param relative_to, 获取元素相对于屏幕或所在窗口的位置信息, 默认相对于屏幕
            * `'screen'`, 相对于屏幕左上角
            * `'window'`, 相对于浏览器客户区域左上角
        * @return `typing.Tuple`, 返回网页元素的位置信息, 如('x', 'y', 'width', 'height')
        '''

        bd = self._invoke('GetBounding', {'to96dpi': to96dpi, 'relativeTo':relative_to})
        return (bd['x'], bd['y'], bd['width'], bd['height'])

    def get_anchor_position(self, *, anchor=None, to96dpi=True) -> typing.Tuple:
        '''
        获取网页元素的锚点属性组合
        * @param anchor, 锚点, 要获取坐标在元素中的的位置以及偏移量元组, 可为 `None`, 默认值为 `None` 为 `None` 时默认获取元素中心位置且无偏移量, 参数结构如下:
            * `'sudoku_part'`, 获取坐标在元素中的位置, 默认获取元素中心位置
                * `'topLeft'`, 获取左上角位置
                * `'topCenter'`, 获取上中部位置
                * `'topRight'`, 获取右上角位置
                * `'middleLeft'`, 获取左中部位置
                * `'middleCenter'`, 获取中心位置
                * `'middleRight'`, 获取中部位置
                * `'bottomLeft'`, 获取下角位置
                * `'bottomCenter'`, 获取下中部位置
                * `'bottomRight'`, 获取右下角位置
                * `'random'`, 随机在元素矩形范围内选择锚点
            * `'offset_x'`, 获取位置的水平偏移量
            * `'offset_y'`, 获取位置的垂直偏移量
        * @param to96dpi, 是否需要将锚点属性转换成dpi为96的对应属性值
        * @return `typing.Tuple`, 返回网页元素的锚点属性组合, 如('x', 'y')
        '''

        sudoku_part, offset_x, offset_y = (
            'middleCenter', 0, 0) if anchor is None else anchor

        ap = self._invoke('GetAnchorPosition', {'sudokuPart': sudoku_part,
                                                'offsetX': offset_x,
                                                'offsetY': offset_y,
                                                'to96dpi': to96dpi})
        return (ap['x'], ap['y'])

    def extract_table(self) -> typing.List[typing.List[str]]:
        '''
        获取当前元素所属表格的内容列表
        * @return `typing.List[typing.Tuple]`, 返回数据表格内容
        '''

        table = self._invoke('GetTable')
        return [tuple(x) for x in table]

    def screenshot(self, folder_path, *, filename=None) -> typing.NoReturn:
        '''
        对目标元素进行截图, 并将图片进行保存
        * @param folder_path, 元素截图后图片需要保存的路径
        * @param filename, 截图后图片保存后的名称, 可为空, 为空时会根据当前时间自动生成文件名称
        '''

        valid('保存文件夹', folder_path, ValidPattern.NotEmpty)
        self._invoke('Screenshot', {
                     'folderPath': folder_path, 'fileName': filename})

    def screenshot_to_clipboard(self) -> typing.NoReturn:
        '''
        对目标元素进行截图, 并将图片添加到剪切板中
        '''

        self._invoke('ScreenshotToClipboard')

    def is_checked(self) -> bool:
        '''
        判断网页复选框元素是否被选中
        * @return `bool`, 返回元素的选中状态, 选中返回`True`, 否则返回`False`
        '''

        return self._invoke('IsChecked')

    def is_enabled(self) -> bool:
        '''
        判断网页元素是否可用
        * @return `bool`, 返回网页元素的可用状态, 可用返回`True`, 否则返回`False`
        '''

        return self._invoke('IsEnabled')

    def is_displayed(self) -> bool:
        '''
        判断网页元素是否可见
        * @return `'bool'`, 返回网页元素的可见性, 可见返回`True`不可见返回`False` 
        '''

        return self._invoke('IsDisplayed')

    def execute_javascript(self, code, argument=None) -> typing.Any:
        '''
        在当前元素上执行Javascript脚本
        * @param code, 要执行的JS脚本，必须为javascript函数形式，如:
        ```python
        """
        function (element, args) {
            // element表示当前元素(HTML元素)
            // args表示输入的参数
            return args;
        }
        """
        ```
        * @param argument, 要传入到JS函数中的参数，必须为字符串，如果需要传入其他类型可以先将其转为JSON字符串形式
        * @return `Any`, 返回JS脚本执行结果
        '''

        # js执行异常，这里会抛出UIAError
        return self._invoke('ExecuteJavaScript', {'argument': argument, 'code': code})

    def scroll_to(self, *, location='bottom', behavior='instant', top=0, left=0) -> typing.NoReturn:
        '''
        在当前网页指定的元素上滚动鼠标滚轮
        * @param location, 滚动位置, 默认滚动到底部
            * `'bottom'`, 滚动到底部,
            * `'top'`, 滚动到顶部
            * `'point'`, 滚动到指定位置 
        * @param behavior, 滚动效果, 默认平滑滚动
            * `'smooth'`, 平滑滚动
            * `'instant'`, 瞬间滚动
        * @param top, 滚动到指定位置的纵坐标
        * @param left, 滚动到指定位置的横坐标
        '''

        # location: point(滚动到指定位置top/left), bottom(滚动到底部), top(滚动到顶部)
        # behavior：smooth(平滑滚动), instant(瞬间滚动)
        self._invoke(
            'ScrollTo', {'location': location, 'behavior': behavior, 'top': top, 'left': left})

    def drag_to(self, *, simulative=True, behavior='smooth', top=0, left=0, delay_after=1, anchor=None) -> typing.NoReturn:
        '''
        拖拽网页元素到指定位置
        * @param simulative, 是否模拟人工拖拽, 默认值为True模拟人工
        * @param behavior, 滚动效果, 默认平滑滚动
            * `'smooth'`, 平滑拖拽
            * `'instant'`, 瞬间拖拽
        * @param top, 相对于当前元素中心的纵向位移
        * @param left, 相对于当前元素中心的横向位移
        * @param delay_after：指令执行成功后延迟执行时间，默认值为1s
        * @param anchor, 锚点, 鼠标在拖拽元素中按下的位置以及偏移量元组, 可为 `None`, 默认值为 `None` 为 `None` 时默认在元素中心按下且无偏移量, 参数结构如下:
            * `'sudoku_part'`, 鼠标在拖拽元素中按下的部位, 默认在拖拽元素的中心位置按下
                * `'topLeft'`, 拖拽元素的左上角按下
                * `'topCenter'`, 拖拽元素的上中部按下
                * `'topRight'`, 拖拽元素的右上角按下
                * `'middleLeft'`, 拖拽元素的左中部按下
                * `'middleCenter'`, 拖拽元素的中心按下
                * `'middleRight'`, 拖拽元素的中部按下
                * `'bottomLeft'`, 拖拽元素的左下角按下
                * `'bottomCenter'`, 拖拽元素的中下部按下
                * `'bottomRight'`, 拖拽元素的右下角按下
                * `'random'`, 随机在拖拽元素矩形范围内选择锚点
            * `'offset_x'`, 鼠标按下位置的水平偏移量
            * `'offset_y'`, 鼠标按下位置的垂直偏移量
        '''

        sudoku_part, offset_x, offset_y = (
            'middleCenter', 0, 0) if anchor is None else anchor
        self._invoke(
            'DragTo', {'simulative': simulative,
                       'top': top,
                       'left': left,
                       'sudokuPart': sudoku_part,
                       'offsetX': offset_x,
                       'offsetY': offset_y})
        if delay_after > 0:
            time.sleep(delay_after)

    def upload(self, file_names, *, simulative=False, clipboard_input=True, dialog_timeout=20, force_ime_ENG=False, send_key_delay=50, focus_timeout=1000) -> typing.NoReturn:
        '''
        上传文件
        * @param file_names, 要上传文件完整路径; 如果需要多文件上传, 输入完整路径数组，比如: [r"C:\test.txt",r"C:\text1.txt"]
        * @param simulative, 模拟输入: 通过模拟人工的方式触发输入事件; 非模拟输入(自动化接口输入): 调用元素自身实现的自动化接口输入; 默认值为`False`
        * @param clipboard_input, 是否使用剪切板输入文件路径
        * @param dialog_timeout, 点击上传按钮后，等待文件选择框的最大时间, 默认为20s
        * @param force_ime_ENG, 使用模拟输入时会自动切换当前输入法为英文输入状态, 以避免输入法造成的输入错误问题。存在不常见的输入法切换英文输入状态不成功的情况, 需要指定强制加载美式键盘(ENG), 确保模拟输入不受中文输入法影响, 默认值为`False`
        * @param send_key_delay, 两次按键之间的时间间隔(仅模拟输入有效, 对影刀浏览器该参数无效)，默认为50ms
        * @param focus_timeout, 焦点超时时间(获取焦点和输入操作的间隔), 默认为1000ms
        '''
        if isinstance(file_names, str):
            file_names = [file_names]

        valid_multi('获取焦点等待时间', focus_timeout, [
                    (ValidPattern.Type, int),
                    (ValidPattern.Min, -1)])
        valid_multi('等待文件选择框超时时间', dialog_timeout, [
                    (ValidPattern.Type, int),
                    (ValidPattern.Min, -1)])
        try:
            automation = self._create_automation()
            # step 1: 点击弹框前，先做一些设置
            automation.before_file_dialog_open(choose_file_names=file_names)

            # step 2: 点击
            self.click(simulative=True)

            # step 3: 处理弹框部分(打开->输入->关闭)
            automation.choose_file_dialog(file_names,
                                          simulative=simulative,
                                          clipboard_input=clipboard_input,
                                          wait_appear_timeout=dialog_timeout,
                                          force_ime_ENG=force_ime_ENG,
                                          send_key_delay=send_key_delay,
                                          focus_timeout=focus_timeout)
        finally:
            # step 4:关闭框后处理，释放资源
            automation.after_file_dialog_closed()

    def download(self, file_folder, *, file_name=None, wait_complete=True, wait_complete_timeout=300, simulative=False, clipboard_input=True, dialog_timeout=20, force_ime_ENG=False, send_key_delay=50, focus_timeout=1000) -> str:
        '''
        下载文件
        * @param file_folder, 保存下载文件的文件夹
        * @param file_name, 保存文件名, 为None时, 使用下载资源默认文件名, 若无默认文件名则自动为下载资源生成不重复的文件名
        * @param wait_complete, 是否等待下载完成，默认为False
        * @param wait_complete_timeout,等待下载超时时间，单位(秒)
        * @param simulative, 模拟输入: 通过模拟人工的方式触发输入事件; 非模拟输入(自动化接口输入): 调用元素自身实现的自动化接口输入; 默认值为`False`
        * @param clipboard_input, 是否使用剪切板输入文件路径
        * @param dialog_timeout, 点击上传按钮后，等待文件选择框的最大时间, 默认为20s
        * @param force_ime_ENG, 使用模拟输入时会自动切换当前输入法为英文输入状态, 以避免输入法造成的输入错误问题。存在不常见的输入法切换英文输入状态不成功的情况, 需要指定强制加载美式键盘(ENG), 确保模拟输入不受中文输入法影响, 默认值为`False`
        * @param send_key_delay, 两次按键之间的时间间隔，默认为50ms
        * @param focus_timeout, 焦点超时时间(获取焦点和输入操作的间隔), 默认为1000ms
        * @return `str`, 下载完成的文件完整路径
        '''
        valid_multi('等待下载超时时间', wait_complete_timeout, [
                    (ValidPattern.Type, int),
                    (ValidPattern.Min, -1)])
        valid_multi('获取焦点等待时间', focus_timeout, [
                    (ValidPattern.Type, int),
                    (ValidPattern.Min, -1)])
        valid_multi('等待文件选择框超时时间', dialog_timeout, [
                    (ValidPattern.Type, int),
                    (ValidPattern.Min, -1)])

        try:
            automation = self._create_automation()
            # step 1: 点击弹框前，先做一些设置
            automation.before_file_dialog_open(
                saveAs_file_folder=file_folder, saveAs_file_name=file_name)

            # step 2: 点击
            self.click(simulative=True)

            # step 3: 处理弹框部分(打开->输入->关闭)
            download_file_name = automation.saveAs_file_dialog(file_folder,
                                                               file_name=file_name,
                                                               simulative=simulative,
                                                               clipboard_input=clipboard_input,
                                                               wait_appear_timeout=dialog_timeout,
                                                               force_ime_ENG=force_ime_ENG,
                                                               send_key_delay=send_key_delay,
                                                               focus_timeout=focus_timeout)

            # step 4:等待加载完成
            if wait_complete:
                task_id = automation.download_task_id()
                for _ in Retry(wait_complete_timeout, interval=0.5, error_message='等待下载完成超时'):
                    if automation.is_download_complete(task_id):
                        break
            return download_file_name
        finally:
            # step 5:关闭框后处理，释放资源
            automation.after_file_dialog_closed()

    @abc.abstractmethod
    def _create_element(self, bid, eid):
        pass

    @abc.abstractmethod
    def _create_automation(self):
        pass

    def _invoke(self, action, args=None):
        all_args = {'browserId': self.bid, 'elementId': self.eid}
        if args is not None:
            all_args.update(args)
        return uidriver.execute(f'{self._controller}.{action}', all_args)
