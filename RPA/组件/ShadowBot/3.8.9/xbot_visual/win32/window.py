from .._core import visual_action, parseint_from_args
from xbot.selector import Selector
from xbot import win32
from xbot.win32.window import Win32Window
from xbot.win32.element import Win32Element

import typing
import time


@visual_action
def get(**args):
    """
    {
        'window_type': 'window_selector/win_handle/win_title_or_class'
        'selector': selector
        'handle': handle
        'title': str
        'class_name': str
        'use_wildcard': True/False
    }
    """
    return _get_window_by_type(args)


def get_details(**args) -> str:  # to do 获取窗口大小和位置
    '''
    {
        'window_type': 'window_instance/window_selector/win_handle/win_title_or_class'
        'window': win32window
        'selector': selector
        'handle': handle
        'title': str
        'class_name': str
        'use_wildcard': True/False
        'operation': 'title/text/process_name'       
    }
    '''
    window = _get_window_by_type(args)
    return window.get_detail(args['operation'])


@visual_action
def activate(**args) -> typing.NoReturn:
    """
    {
        'window_type': 'window_instance/window_selector/win_handle/win_title_or_class'
        'window': win32window
        'selector': selector
        'handle': handle
        'title': str
        'class_name': str
        'use_wildcard': True/False
    }
    """
    window = _get_window_by_type(args)
    window.activate()


@visual_action
def set_state(**args) -> typing.NoReturn:
    """
    {
        'window_type': 'window_instance/window_selector/win_handle/win_title_or_class'
        'window': win32window
        'selector': selector
        'handle': handle
        'title': str
        'class_name': str
        'use_wildcard': True/False
        'flag': 'minimize/maximize/restore'
    }
    """
    window = _get_window_by_type(args)
    window.set_state(args["flag"])


@visual_action
def set_visibility(**args) -> typing.NoReturn:
    """
    {
        'window_type': 'window_instance/window_selector/win_handle/win_title_or_class'
        'window': win32window
        'selector': selector
        'handle': handle
        'title': str
        'class_name': str
        'use_wildcard': True/False
        'flag': 'hide/show'
    }
    """
    window = _get_window_by_type(args)
    window.set_state(args["flag"])


@visual_action
def move(**args) -> typing.NoReturn:
    '''    
    {
        'window_type': 'window_instance/window_selector/win_handle/win_title_or_class'
        'window': win32window
        'selector': selector
        'handle': handle
        'title': str
        'class_name': str
        'use_wildcard': True/False
        'x': x 
        'y': y
    }
    '''
    x = parseint_from_args(args, 'x')
    y = parseint_from_args(args, 'y')
    window = _get_window_by_type(args)
    window.move(x=x, y=y)


@visual_action
def resize(**args) -> list:
    """
    {
        'window_type': 'window_instance/window_selector/win_handle/win_title_or_class'
        'window': win32window
        'selector': selector
        'handle': handle
        'title': str
        'class_name': str
        'use_wildcard': True/False
        'width': width
        'height': height
    }
    """
    width = parseint_from_args(args, 'width')
    height = parseint_from_args(args, 'height')
    window = _get_window_by_type(args)
    window.resize(width=width, height=height)


@visual_action
def close(**args) -> typing.NoReturn:
    """
    {
        'window_type': 'window_instance/window_selector/win_handle/win_title_or_class'
        'window': win32window
        'selector': selector
        'handle': handle
        'title': str
        'class_name': str
        'use_wildcard': True/False
    }
    """
    window = _get_window_by_type(args)
    window.close()


@visual_action
def contains_element(**args) -> bool:
    """
    {
        'window': ,
        'content_type': 'contains_element/not_contains_element',
        'element': selector or element,
        'text':''
    }
    """
    window = _window(args)[0]
    content_type = args["content_type"]

    def contains_selector_or_element(selector_or_element):
        if isinstance(selector_or_element, Selector):
            return window.contains_element(selector_or_element)
        elif isinstance(selector_or_element, Win32Element):
            return True
        else:
            raise ValueError("selector参数类型不正确")

    if content_type == "contains_element":
        return contains_selector_or_element(args["element"])
    elif content_type == "not_contains_element":
        return not contains_selector_or_element(args["element"])
    else:
        raise ValueError(f"无效的检测内容类型{content_type}")

def exists(**args):
    try:
        window = _get_window_by_type(args)
    except:
        window = None
    window_status = args['window_status']

    if window_status == "existed":
        return win32.exists(window)
    if window_status == "not_existed":
        return not win32.exists(window)

def wait_window(**args):
    use_timeout = args['use_timeout']
    wait_way = args['wait_way']
    if not use_timeout:
        args['timeout'] = '-1'

    try:
        window = _get_window_by_type(args)
    except:
        window = None

    timeout = parseint_from_args(args, 'timeout')
    if wait_way == 'appear':
        return window is not None       
    elif wait_way == 'disappear':
        if window is None:
            return True
        else:
            return window.wait_close(timeout=timeout)
    elif wait_way == 'be_focus':
        if window is None:
            return False
        else:
            return window.wait_focus(timeout=timeout)
    elif wait_way == 'lost_focus':
        if window is None:
            return True
        else:
            return window.wait_focusout(timeout=timeout)


def _get_window_by_type(args):
    win_type = args['window_type']
    timeout = parseint_from_args(args, 'timeout', default=5)
    if win_type == 'window_instance':
        window = args['window']
        if isinstance(window, Win32Window):
            return window
        else:
            raise ValueError(f'窗口类型错误{win_type} : {window}')

    elif win_type == 'window_selector':
        window = args['selector']
        if isinstance(window, Selector):
            return win32.get_by_selector(window, timeout=timeout)
        else:
            raise ValueError(f'窗口类型错误{win_type} : {window}')

    elif win_type == 'win_handle':
        window = args['handle']
        if isinstance(window, str):
            dec_handle = int(window, 16)
            return win32.get_by_handle(dec_handle, timeout=timeout)
        else:
            raise ValueError(f'窗口类型错误{win_type} : {window}')

    elif win_type == "win_title_or_class":
        return win32.get(args["title"], args["class_name"], args.get('use_wildcard', False), timeout=timeout)

    elif win_type == "desktop":
        return win32.get_desktop()

    else:
        raise ValueError(f"无效的检测内容类型{win_type}")

def _window(args):
    return [args["window"]]
