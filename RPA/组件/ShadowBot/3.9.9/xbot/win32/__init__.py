'''
Win32处理模块，主要用来处理win32窗口、win32元素等
'''

from . import clipboard, element, image, screenshot, window

from .._core.retry import Retry as _Retry
from .._core.validation import valid as _valid, ValidPattern as _ValidPattern
from .._core.uidriver import execute as _execute
from ..selector import Selector, _get_selector_by_name
from ..errors import UIAError, UIAErrorCode
from .window import Win32Window
from .element import Win32Element

import typing
import time

import os, typing, base64, time, json, win32api, win32gui, winerror, win32event, win32process, ctypes


def get(title=None, class_name=None, use_wildcard=False, *, timeout=5) -> Win32Window:
    """
    根据指定的标题或类名获取窗口对象, 默认是使用模糊匹配, 如果`use_wildcard`为`True`则使用通配符匹配
    * @param title, 指定的窗口标题
    * @param class_name, 指定的窗口类名
    * @param use_wildcard, 是否使用通配符进行匹配, 默认值为`False`
    * @param timeout, 获取窗口对象超时时间, 默认值是5s, 如果超过改时间还未找到窗口在抛出 `UIAError` 的异常
        * 等于 0, 不等待
        * 大于 0, 按时间等待
        * 等于 -1, 一直等待
    * @return `Win32Window`, 获取到的窗口对象
    """

    if title is None and class_name is None:
        raise ValueError('标题或类型名至少指定一个')
    for _ in _Retry(timeout=timeout, interval=0.5, error_message='获取窗口失败'):
        try:
            wid = _invoke('GetWindowByTitleAndClassName', {
                          'title': title, 'className': class_name, 'useWildcard': use_wildcard})
            window = _create_window(wid)
            return window
        except UIAError as e:
            if e.code == UIAErrorCode.NoSuchWindow:
                pass
            else:
                raise e


def get_by_handle(handle=None, *, timeout=5) -> Win32Window:
    """
    根据指定的窗口句柄获取窗口对象
    * @param handle, 指定的窗口句柄获, 是一个十六进制的数, 如 0x14210c
    * @param timeout, 获取窗口对象超时时间, 默认值是5s, 如果超过改时间还未找到窗口在抛出 `UIAError` 的异常
        * 等于 0, 不等待
        * 大于 0, 按时间等待
        * 等于 -1, 一直等待
    * @return `Win32Window`, 获取到的窗口对象
    """

    _valid('handle', handle, (_ValidPattern.Type, int))
    for _ in _Retry(timeout=timeout, interval=0.5, error_message='获取窗口失败'):
        try:
            wid = _invoke('GetWindowByHandle', {'handle': handle})
            window = _create_window(wid)
            return window
        except UIAError as e:
            if e.code == UIAErrorCode.NoSuchWindow:
                pass
            else:
                raise e


def get_by_selector(selector=None, *, timeout=5) -> Win32Window:
    """
    查找并返回与选择器匹配的窗口对象
    * @param selector, 要查找的选择器, 支持以下格式: 
        * 选择器名称, `str`类型
        * 选择器对象, `Selector`类型
    * @param timeout, 获取窗口对象超时时间, 默认值是5s, 如果超过改时间还未找到窗口在抛出 `UIAError` 的异常
        * 等于 0, 不等待
        * 大于 0, 按时间等待
        * 等于 -1, 一直等待
    * @return `Win32Window`, 返回与选择器配的窗口对象
    """

    if isinstance(selector, str):
        selector = _get_selector_by_name(selector)
    _valid('selector', selector, (_ValidPattern.Type, Selector))
    for _ in _Retry(timeout=timeout, interval=0.5, error_message='获取窗口失败'):
        try:
            wid = _invoke('GetWindowBySelector', {'selector': selector.value})
            window = _create_window(wid)
            return window
        except UIAError as e:
            if e.code == UIAErrorCode.NoSuchWindow:
                pass
            else:
                raise e

def get_by_element(element) -> Win32Window:
    if isinstance(element, Win32Element):
        return element.window

def get_desktop() -> Win32Window:
    """
    获取桌面对象
    * @return `Win32Window`, 获取到的桌面对象
    """

    for _ in _Retry(5, interval=0.5, error_message='获取窗口失败'):
        try:
            wid = _invoke('GetDesktopWindow')
            window = _create_window(wid)
            return window
        except UIAError as e:
            if e.code == UIAErrorCode.NoSuchWindow:
                pass
            else:
                raise e


def get_active() -> Win32Window:
    """
    获取当前激活窗口的对象
    * @return `Win32Window`, 获取到的窗口对象
    """

    for _ in _Retry(5, interval=0.5, error_message='获取窗口失败'):
        try:
            wid = _invoke('GetActiveWindow')
            window = _create_window(wid)
            return window
        except UIAError as e:
            if e.code == UIAErrorCode.NoSuchWindow:
                pass
            else:
                raise e


def minimize_all():
    """
    最小化全部窗口
    """

    _invoke("MinimizeAllWindows")


def mouse_move(point_x: int, point_y: int, relative_to='screen', move_speed='instant', delay_after=1):
    """
    移动鼠标到指定位置
    * @param point_x, 指定坐标的横坐标, 为整数
    * @param point_y, 指定坐标的纵坐标, 为整数
    * @param relative_to, 指定坐标位置的相对对象, 默认相对于桌面移动
        * `'screen'`, 相对于桌面
        * `'window'`, 相对于当前打开(激活)的窗口
        * `'position'`, 相对于当前数据所在的位置
    * @param move_speed, 移动鼠标到指定坐标的速度, 默认瞬间移动到目标坐标
        * `'instant'`, 瞬间
        * `'fast'`, 快速
        * `'middle'`, 中速
        * `'slow'`, 慢速
    * @param delay_after, 执行成功后延迟时间, 默认延迟1s
    """

    _invoke("MouseMove", {'pointX': point_x, 'pointY': point_y,
                          'relativeTo': relative_to, 'moveSpeed': move_speed})
    if delay_after > 0:
        time.sleep(delay_after)


def mouse_move_by_anchor(rectangle, anchor=None, relative_to='screen', move_speed='instant', delay_after=1):
    """
    移动鼠标到指定位置
    * @param rectangle, 需要悬浮的目标矩形范围，格式为 (x, y, width, height)
    * @param anchor, 锚点位置，默认值为 ('middleCenter', 0, 0)，表示悬浮在范围的中心，不偏移
    * @param relative_to, 指定坐标位置的相对对象, 默认相对于桌面移动
        * `'screen'`, 相对于桌面
        * `'window'`, 相对于当前打开(激活)的窗口
        * `'position'`, 相对于当前数据所在的位置
    * @param move_speed, 移动鼠标到指定坐标的速度, 默认瞬间移动到目标坐标
        * `'instant'`, 瞬间
        * `'fast'`, 快速
        * `'middle'`, 中速
        * `'slow'`, 慢速
    * @param delay_after, 执行成功后延迟时间, 默认延迟1s
    """
    
    sudoku_part, offset_x, offset_y = ('middleCenter', 0, 0) if anchor is None else anchor
    x, y, width, height = rectangle

    _invoke('MouseMoveByAnchor', {
                                    'rectangle': {'x': x, 'y': y, 'width': width, 'height': height},
                                    'sudokuPart': sudoku_part,
                                    'offsetX': offset_x,
                                    'offsetY': offset_y,

                                    'relativeTo': relative_to,
                                    'moveSpeed': move_speed
                                 }
    )

    if delay_after > 0:
        time.sleep(delay_after)


def send_keys(keys='', send_key_delay=50, hardware_driver_input=False, delay_after=1):
    """
    给当前激活窗口发送文本: 对于默认输入方式: !、#、+、^、{、} 这六个特殊符号,请用{}包括起来, 如{#}、{{}等; 对于驱动输入方式: 只支持键盘上的可见字符, 不能用此方式发送特殊按键, 比如Tab、Ctr、Enter、Shift...
    * @param keys, 键盘按键
    * @param hardware_driver_input, 是否通过硬件驱动的方式输入
    * @param send_key_delay, 两次按键之间的时间间隔，默认为50ms
    * @param delay_after, 执行成功后延迟时间, 默认延迟1s
    """

    _invoke("SendKeys", {'keys': keys, "hardwareDriverInput": hardware_driver_input, "sendKeyDelay": send_key_delay})
    if delay_after > 0:
        time.sleep(delay_after)


def mouse_click(button='left', click_type='click', hardware_driver_click=False, keys='none', delay_after=1):
    """
    模拟鼠标点击, 如鼠标左键单击、左键双击等
    * @param button, 要点击的鼠标按键, 默认为左键
        * `'left'`, 鼠标左键
        * `'right'`, 鼠标右键
    * @param click_type, 鼠标按键的点击方式, 如单击、双击等, 默认为单击
        * `'click'`, 鼠标单击
        * `'dbclick'`, 鼠标双击
        * `'down'`, 鼠标按键按下
        * `'up'`, 鼠标按键弹起
    * @param hardware_driver_click, 是否通过硬件驱动的方式点击
    * @param keys, 点击鼠标按钮时的键盘辅助按钮，可以为空，默认为空
        * `'none'`, 无键盘辅助按钮
        * `'alt'`, 使用`alt`键作为辅助按钮
        * `'ctrl'`, 使用 `ctrl`键作为辅助按钮
        * `'shift'`, 使用`shift`键作为辅助按钮
        * `'win'`, 使用win(窗口)键作为辅助按钮
    * @param delay_after, 执行成功后延迟时间, 默认延迟1s
    """

    _invoke('MouseClick', {'button': button,
                           'clickType': click_type, "hardwareDriverClick": hardware_driver_click, 'keys': keys})
    if delay_after > 0:
        time.sleep(delay_after)


def mouse_click_by_anchor(rectangle, anchor=None, button='left', click_type='click', keys='none', hardware_driver_click=False, delay_after=1, move_mouse=True):
    """
    模拟鼠标点击指定位置, 如鼠标左键单击、左键双击等
    * @param rectangle, 需要点击的目标矩形范围，格式为 (x, y, width, height)
    * @param anchor, 锚点位置，默认值为 ('middleCenter', 0, 0)，表示点击范围的中心，不偏移
    * @param button, 要点击的鼠标按键, 默认为左键
        * `'left'`, 鼠标左键
        * `'right'`, 鼠标右键
    * @param click_type, 鼠标按键的点击方式, 如单击、双击等, 默认为单击
        * `'click'`, 鼠标单击
        * `'dbclick'`, 鼠标双击
        * `'down'`, 鼠标按键按下
        * `'up'`, 鼠标按键弹起
    * @param hardware_driver_click, 是否通过硬件驱动的方式点击
    * @param keys, 点击鼠标按钮时的键盘辅助按钮，可以为空，默认为空
        * `'none'`, 无键盘辅助按钮
        * `'alt'`, 使用`alt`键作为辅助按钮
        * `'ctrl'`, 使用 `ctrl`键作为辅助按钮
        * `'shift'`, 使用`shift`键作为辅助按钮
        * `'win'`, 使用win(窗口)键作为辅助按钮
    * @param delay_after, 执行成功后延迟时间, 默认延迟1s
    * @param move_mouse, 是否显示鼠标移动轨迹, 默认为`True`，显示鼠标移动轨迹
    """

    sudoku_part, offset_x, offset_y = ('middleCenter', 0, 0) if anchor is None else anchor
    x, y, width, height = rectangle

    _invoke('MouseClickByAnchor', {
                            'rectangle': {'x': x, 'y': y, 'width': width, 'height': height},
                            'sudokuPart': sudoku_part,
                            'offsetX': offset_x,
                            'offsetY': offset_y,
                            
                            'button': button,
                            'clickType': click_type, 
                            'keys': keys,
                            "hardwareDriverClick": hardware_driver_click,

                            'moveMouse': move_mouse
                           }
    )

    if delay_after > 0:
        time.sleep(delay_after)


def mouse_wheel(wheel_direction='down', wheel_times=1, keys='none', delay_after=1):
    """
    模拟鼠标滚轮滚动, 默认往下滚动
    * @param wheel_direction, 鼠标滚轮滚动方向, 默认往下滚动
        * `'up'`, 往上滚动鼠标滚轮
        * `'down'`, 往下滚动鼠标滚轮
    * @param wheel_times, 滚动鼠标滚轮次数，默认滚动1次
    * @param keys, 滚动鼠标滚轮时的键盘辅助按钮，可以为空，默认为空
        * `'none'`, 无键盘辅助按钮
        * `'alt'`, 使用`alt`键作为辅助按钮
        * `'ctrl'`, 使用 `ctrl`键作为辅助按钮
        * `'shift'`, 使用`shift`键作为辅助按钮
        * `'win'`, 使用win(窗口)键作为辅助按钮
    * @param delay_after, 执行成功后延迟时间, 默认延迟1s
    """

    _invoke('MouseWheel', {'wheelDirection': wheel_direction,
                           'wheelTimes': wheel_times, 'keys': keys})
    if delay_after > 0:
        time.sleep(delay_after)


def get_mouse_position(relative_to='screen') -> typing.Tuple:
    """
    获取鼠标相对于桌面/当前选中(激活)的窗的坐标位置
    * @param relative_to, 获取元素相对于屏幕或所在窗口的位置信息, 默认相对于屏幕
        * `'screen'`, 相对于屏幕左上角
        * `'window'`, 相对于激活窗口左上角
    * @return `tuple`, 返回一组坐标值
    """
    position = _invoke("GetMousePosition", {'relativeTo': relative_to})
    return (position['x'], position['y'])


def exists(window) -> bool:
    '''
    判断窗口是否存在
    * @param window, Win32Window窗口对象
    * @return `bool`, 返回窗口的存在窗台, 存在返回`True`, 否则返回`False`
    '''

    if window is None:
        return False
    if not isinstance(window, Win32Window):
        return False
    return _invoke('Exists', {'hWnd': window.hWnd})


def get_selected_text(wait_time = 0, **kwargs) -> str:             
    '''
    获取当前激活窗口选中的文本
    * @return `str`, 返回当前激活窗口选中的文本
    '''
    return _invoke('GetSelectedText', {'waitTime': int(wait_time)})


def _invoke(action, args=None):
    return _execute(f'Win32.{action}', args)


def _create_window(wid) -> Win32Window:
    return Win32Window('Win32Window', wid)


def lock_screen() -> typing.NoReturn:
    '''
    屏幕锁屏
    '''
    ctypes.windll.user32.LockWorkStation()


def _credential_provider_running():
    mutex_name = 'shadowbot_credential_provider_running'
    mutex = win32event.CreateMutex(None, False, mutex_name)
    is_running = (winerror.ERROR_ALREADY_EXISTS == win32api.GetLastError())
    win32api.CloseHandle(mutex)
    return is_running

def unlock_screen(user_name, password) -> typing.NoReturn:
    '''
    屏幕解屏
    * @param user_name, 用户名
    * @param password, 密码
    '''

    path = ctypes.create_unicode_buffer(1024)
    ctypes.windll.Kernel32.GetEnvironmentVariableW('ProgramData', path, 1024)
    path = os.path.join(path.value, r'ShadowBot\support\CredentialProvider')

    #检查是否已经安装 credential provider 
    versiontxt_path = os.path.join(path, r'Version.txt')
    if not os.path.exists(versiontxt_path):
        raise ValueError('屏幕解锁服务尚未安装，请在“托盘右键菜单>设置>工具>屏幕解锁服务”中安装。')
    with open(versiontxt_path, 'r') as f:
        version = f.readline()
        if version != '1.0.0.1':
            raise ValueError('屏幕解锁服务版本过低，请在“托盘右键菜单>设置>工具>屏幕解锁服务”中重新安装。')

    #程序是否正在运行
    if not _credential_provider_running():
        return
        
    #写入用户名和密码    
    rdptxt_path = os.path.join(path, r'Credential.txt')
    with open(rdptxt_path, 'w') as f:
        password_base64 = base64.b64encode(password.encode('ANSI')).decode()
        #写入文件时，python 会将 \n 自动转换成 \r\n
        text = f'{user_name}\n{password_base64}'
        f.write(text)

    #等待解屏
    for i in range(5):  
        time.sleep(1)

        #是否登陆成功
        if not _credential_provider_running():
            return
        
    raise ValueError('屏幕解屏失败！')

def _is_inputlang_valid(window):
    thread_id, _ = win32process.GetWindowThreadProcessId(window)
    hkl = win32api.GetKeyboardLayout(thread_id)

    name = ctypes.create_unicode_buffer(100)
    ctypes.windll.Imm32.ImmGetDescriptionW(hkl, name, 100)

    return '必应 Bing 输入法' not in name.value and 'QQ五笔输入法' not in name.value

def set_ime(lang) -> typing.NoReturn:
    '''
    设置激活窗口的输入法
    * @param lang, 取值为"chinese"或者"english"
    '''
    if lang not in ["chinese","english"]:
        raise ValueError(f'设置输入法参数错误: {lang}')
    _invoke('SetForegroundWinIME', {'lang': lang})


def get_ime() -> str:
    '''
    获取激活窗口的输入法
    * @return `str`, 返回中文"chinese"/英文"english"/未知"unknow"
    '''
    return _invoke('GetForegroundWinIME')