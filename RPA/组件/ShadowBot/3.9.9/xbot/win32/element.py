from __future__ import annotations
from .._core import uidriver
from .._core.retry import Retry
from .._core.validation import valid, valid_multi, ValidPattern
from ..selector import Selector
from ..errors import UIAError, UIAErrorCode

import abc
import typing
import time


class Win32Element(metaclass=abc.ABCMeta):
    '''
    win32元素自动化模块
    '''

    def __init__(self, controller, eid, window):
        self._controller = controller
        self.eid = eid
        self.window = window

    def __del__(self):
        _win32_elements_cache.append(self.eid)

    def click(self, button='left', simulative=True, keys='none', delay_after=1, move_mouse=True, anchor=None) -> typing.NoReturn:
        '''
        单击win32元素
        * @param button, 单击时鼠标按下的按键, 默认为鼠标左键
            * `'left'`, 鼠标左键
            * `'right'`, 鼠标右键
        * @param simulative, 是否模拟人工点击, 默认为`True`, 模拟人工点击
        * @param keys, 鼠标单击时使用的键盘辅助按键, 如`Alt`键, `Ctrl`键等, 可谓空, 默认为空
            * `'none'`, 不需要键盘辅助按键
            * `'alt'`, 键盘Alt键
            * `'ctrl'`, 键盘Ctrl键
            * `'shift'`, 键盘Shift键
            * `'win'`, 键盘win(窗口)键,
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        * @param move_mouse, 是否显示鼠标移动轨迹, 默认为`True`，显示鼠标移动轨迹
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
        self._invoke('Click', {'button': button,
                               'moveMouse': move_mouse,
                               'simulative': simulative,
                               'keys': keys,
                               'sudokuPart': sudoku_part,
                               'offsetX': offset_x,
                               'offsetY': offset_y})
        if delay_after > 0:
            time.sleep(delay_after)

    def dblclick(self, simulative=True, delay_after=1, move_mouse=True, anchor=None) -> typing.NoReturn:
        '''
        双击win32元素
        * @param simulative, 是否模拟人工点击, 默认为`True`, 模拟人工点击
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        * @param move_mouse, 是否显示鼠标移动轨迹, 默认为`True`，显示鼠标移动轨迹
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
        self._invoke(
            'DblClick', {'simulative': simulative,
                         'moveMouse': move_mouse,
                         'sudokuPart': sudoku_part,
                         'offsetX': offset_x,
                         'offsetY': offset_y})
        if delay_after > 0:
            time.sleep(delay_after)

    def input(self, text: str, simulative=True, append=False, contains_hotkey=False, send_key_delay=50, focus_timeout=1000, delay_after=1, anchor=None, force_ime_ENG=False) -> typing.NoReturn:
        '''
        填写win32输入框
        * @param text, 需要填写到win32输入框中的文本内容
        * @param simulative, 模拟输入: 通过模拟人工的方式触发输入事件; 非模拟输入(自动化接口输入): 调用元素自身实现的自动化接口输入; 默认值为`True`
        * @param append, 是否追加输入, 追加输入会保留输入框中原有内容, 在原有内容最后面追加写入内容，非追加时写入会覆盖输入框中原有内容, 默认值为`False`, 非追加写入
        * @param contains_hotkey, 输入内容是否包含快捷键, 该选项只有在模拟人工输入时起效, 默认值为`False`, 不包含快捷键
        * @param send_key_delay, 两次按键之间的时间间隔，默认为50ms
        * @param focus_timeout, 焦点超时时间(获取焦点和输入操作的间隔), 默认为1000ms
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
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
        * @param force_ime_ENG, 使用模拟输入时会自动切换当前输入法为英文输入状态, 以避免输入法造成的输入错误问题。存在不常见的输入法切换英文输入状态不成功的情况, 需要指定强制加载美式键盘(ENG), 确保模拟输入不受中文输入法影响, 默认值为`False`
        '''

        # 参数处理
        sudoku_part, offset_x, offset_y = (
            'middleCenter', 0, 0) if anchor is None else anchor
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

    def clipboard_input(self, text: str, append=False,  focus_timeout=1000, delay_after=1, anchor=None) -> typing.NoReturn:
        '''
        使用剪切板填写win32输入框(能够有效避免输入法带来的问题)
        * @param text, 需要填写到win32输入框中的文本内容
        * @param append, 是否追加输入, 追加输入会保留输入框中原有内容, 在原有内容最后面追加写入内容，非追加时写入会覆盖输入框中原有内容, 默认值为`False`, 非追加写入
        * @param focus_timeout, 焦点超时时间(获取焦点和输入操作的间隔), 默认为1000ms
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
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

    def hover(self, simulative=True, delay_after=1, anchor=None) -> typing.NoReturn:
        '''
        鼠标悬停在win32元素上
        * param simulative, 是否模拟人工悬停, 模拟人工悬停会有明显的鼠标移动轨迹, 非模拟人工时鼠标会瞬间悬停在win32元素上, 默认值为`True`, 模拟人工悬停
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
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
        self._invoke('Hover', {'sudokuPart': sudoku_part,
                               'offsetX': offset_x,
                               'offsetY': offset_y})
        if delay_after > 0:
            time.sleep(delay_after)

    def check(self, mode='check', delay_after=1) -> typing.NoReturn:
        '''
        设置win32复选框是否选中
        * param mode, win32复选框的设置状态, 默认为`check`选中
            * `'check'`, 选中
            * `'uncheck'`, 取消选中
            * `'toggle'`, 反选, 如当前状态为 'uncheck', 则设置为 'check', 反之如果当前为 'check' 则设置为 'uncheck'
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        '''

        self._invoke('Check', {'mode': mode})
        if delay_after > 0:
            time.sleep(delay_after)

    def select(self, item: str, mode='fuzzy', delay_after=1) -> typing.NoReturn:
        '''
        根据下拉项内容设置win32下拉框内容
        * param item, 要设置的某一项的文本内容
        * param mode, 对设置项文本内容的匹配模式, 默认为模糊匹配
            * `'fuzzy'`, 模糊匹配
            * `'exact'`, 精准匹配
            * `'regex'`, 正则匹配
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        '''

        self._invoke('Select', {'item': item, 'mode': mode})
        if delay_after > 0:
            time.sleep(delay_after)

    def select_by_index(self, index: int, delay_after=1) -> typing.NoReturn:
        '''
        根据目标项的下标设置下拉框内容
        * @param index, 要设置的目标项的下标, 下标位置从0开始
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        '''

        self._invoke('SelectByIndex', {'index': index})
        if delay_after > 0:
            time.sleep(delay_after)

    def get_all_select_items(self) ->typing.List[str]:
        '''
        获取下拉框全部下拉选项
        * @return `typing.List[str]`, 返回下拉框的全部下拉选项列表
        '''

        return self._invoke('GetAllSelectItems')

    def get_selected_item(self) ->typing.List[str]:
        '''
        获取下拉框当前选中项
        * @return `typing.List[str]`, 返回下拉框的当前选中项列表
        '''

        return self._invoke('GetSelectedItem')

    def set_value(self, value: str) -> typing.NoReturn:
        '''
        给win32元素设置值
        * @param value, 要设置给win32元素的文本值
        '''

        self._invoke('SetValue', {'value': value})

    def get_attribute(self, name: str) -> str:
        '''
        获取win32元素的属性值
        * @param name, win32元素的属性值
        * @return `str`, 返回win32元素的目标属性值
        '''

        return self._invoke('GetAttribute', {'name': name})

    def get_all_attributes(self):
        '''
        获取win32元素的全部属性值
        * @return `typing.List[typing.Tuple]`, 返回win32元素的全部属性名与属性值的组合列表
        '''

        attrs = self._invoke('GetAllAttributes')
        return [(x['name'], x['value']) for x in attrs]

    def get_text(self) -> str:
        '''
        获取win32元素的文本内容
        * @return `str`, 返回win32元素的文本内容
        '''

        return self._invoke('GetText')

    def get_value(self) -> str:
        '''
        获取win32元素的详细信息
        * @return `str`, 返回win32元素的详细信息
        '''

        return self._invoke('GetValue')

    def drag_to(self, simulative=True, behavior='smooth', top=0, left=0, delay_after=1, anchor=None) -> typing.NoReturn:
        '''
        将win32元素拖拽到指定位置
        * @param simulative, 是否模拟人工拖拽, 默认人工拖拽会有明显的拖拽移动痕迹, 非模拟人工拖住会瞬间将win32元素拖拽到指定位置, 默认值为`True`模拟人工拖拽
        * @param behavior, 拖拽方式, 默认为平滑拖拽
            * `'smooth'`, 平滑拖拽
            * `'instant'`, 瞬间拖拽
        * @param top, 相对于当前元素中心的纵向位移
        * @param left, 相对于当前元素中心的横向位移
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
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

    def screenshot(self, folder_path, *, filename=None) -> typing.NoReturn:
        '''
        对win32元素进行截图并保存
        * @param folder_path, 截图保存的路径
        * @param filename, 截图保存时的文件名, 可为空, 为空时会更具当前时间自动生成文件名
        '''

        valid('保存文件夹', folder_path, ValidPattern.NotEmpty)
        self._invoke('Screenshot', {
                     'folderPath': folder_path, 'fileName': filename})

    def screenshot_to_clipboard(self) -> typing.NoReturn:
        '''
        对win32元素截图，并将截图添加到剪切板中
        '''

        self._invoke('ScreenshotToClipboard')

    def get_bounding(self, to96dpi=True, relative_to='screen') -> tuple:
        '''
        获取win32元素相对于屏幕或元素所在窗口左上角的位置
        * @param to96dpi, 是否将获取的到元素边框信息转换为96dpi下的值, 默认值为`True`需要转换
        * @param relative_to, 获取元素相对于屏幕或所在窗口的位置信息, 默认相对于屏幕
            * `'screen'`, 相对于屏幕左上角
            * `'window'`, 相对于元素所在窗口左上角
        * @return `tuple`, 返回win32元素位置信息, 如('x', 'y', 'width', 'height')
        '''
        bounding = self._invoke('GetBounding', {'to96dpi': to96dpi, 'relativeTo':relative_to})
        return (bounding['x'], bounding['y'], bounding['width'], bounding['height'])

    def get_anchor_position(self, *, anchor=None, to96dpi=True) -> typing.Tuple:
        '''
        获取win32元素的锚点属性组合
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
    
    def parent(self) -> Win32Element:
        '''
        获取当前元素的父元素
        * @return `Win32Element`, 返回当前元素的父元素
        '''

        eid = self._invoke('Parent')
        return None if eid is None else self._create_element(eid)
    
    def children(self) -> list[Win32Element]:
        '''
        获取当前元素的所有子元素
        * @return `List<Win32Element>`, 返回当前元素的所有子元素
        '''

        eid_list = self._invoke('Children')
        return [self._create_element(eid) for eid in eid_list]
    
    def child_at(self, index) -> Win32Element:
        '''
        获取指定位置的子元素
        * @param index, 子元素的位置索引，从0开始计数
        * @return `Win32Element`, 返回指定位置的子元素
        '''

        eid = self._invoke('ChildAt', {'index': index})
        return None if eid is None else self._create_element(eid)
    
    def next_sibling(self) -> Win32Element:
        '''
        获取下一个并列的兄弟元素
        * @return `Win32Element`, 返回下一个并列的兄弟元素
        '''

        eid = self._invoke('NextSibling')
        return None if eid is None else self._create_element(eid)

    def _create_element(self, eid) -> Win32Element:
        if eid.startswith('SAP'):
            return SAPElement('Win32Element', eid, self.window)
        else:
            return Win32Element('Win32Element', eid, self.window)

    def _invoke(self, action, args=None):
        all_args = {'elementId': self.eid}
        if args is not None:
            all_args.update(args)
        return uidriver.execute(f'{self._controller}.{action}', all_args)

class SAPElement(Win32Element):
    '''
    SAP元素模块
    '''

    def __init__(self, controller, eid, window):
        super().__init__(controller, eid, window)
    
    def expand_tree_and_select_node(self, text_path):
        '''
        扩展树以显示目标节点，然后选中目标节点
        * @param text_path, 填写目标节点的位置路径，如 SAP 菜单/会计核算/控制
        '''

        uidriver.execute('SapElement.ExpandTreeAndSelectNode', {
            'elementId': self.eid,
            'textPath': text_path
        })
    
    def get_table_row_count(self) -> int:
        '''
        获取数据表格总行数
        * @return `int`, 返回获取到的总行数
        '''

        return uidriver.execute('SapElement.GetTableRowCount', {
            'elementId': self.eid
        })
    
    def get_table_column_count(self) -> int:
        '''
        获取数据表格总列数
        * @return `int`, 返回获取到的总列数
        '''

        return uidriver.execute('SapElement.GetTableColumnCount', {
            'elementId': self.eid
        })
    
    def get_table_cell_by_rownum_and_columnnum(self, row_num, column_num) -> SAPElement:
        '''
        获取数据表格指定单元格元素
        * @param row_num, 指定行号, 行号从1开始
        * @param column_num, 指定列号, 列号从1开始
        * @return `SAPElement`, 返回获取到的单元格元素
        '''

        eid = uidriver.execute('SapElement.GetTableCellByRowIndexAndColumnNum', {
            'elementId': self.eid,
            'rowIndex': row_num - 1,
            'columnIndex': column_num - 1
        })
        return None if eid is None else self._create_element(eid)

class _Win32ElementCache(object):
    def __init__(self):
        self._list = list()

    def append(self, item):
        self._list.append(item)

    def release(self):
        if len(self._list) > 0:
            element_ids = self._list.copy()
            self._list.clear()
            uidriver.execute(f'Win32.ReleaseElementCache',
                             {'elementIds': element_ids})


_win32_elements_cache = _Win32ElementCache()
