from typing import NoReturn, Any, List
from .._core import visual_action, parseint_from_args, parsefloat_from_args

from xbot.mobile.element import MobileElement
from xbot.selector import Selector

import re

@visual_action
def get_page_source(**args) -> str:
    """
    {
        'session': session
    }
    """
    return args['session'].get_page_source()

@visual_action
def close(**args) -> NoReturn:
    """
    {
        'session': session
    }
    """
    args['session'].close()

@visual_action
def swipe(**args) -> NoReturn:
    """
    {
        'session': session,
        'swipe_range': 'screen'/'element',
        'element':

        'swipe_kind': 'direction'/'location',

        'swipe_direction': 'up'/'down'/'left'/'right',
        
        'start_point_x': ,
        'start_point_y': ,
        'end_point_x': ,
        'end_point_y': ,

        'swipe_time': 800,
        'delay_after': 1
    }
    """

    # 1、计算滑动的起止位置
    if args['swipe_range'] == "screen":
        if args['swipe_kind'] == 'direction':
            width, height = args['session'].get_window_size()
            start_point_x, start_point_y, end_point_x, end_point_y = _get_swipe_location(
                0, 0, 
                width, height, 
                args['swipe_direction'])
        elif args['swipe_kind'] == 'location':
            start_point_x = parseint_from_args(args, 'start_point_x')
            start_point_y = parseint_from_args(args, 'start_point_y')
            end_point_x = parseint_from_args(args, 'end_point_x')
            end_point_y = parseint_from_args(args, 'end_point_y')
    elif args['swipe_range'] == "element":
        element = _element(args)
        bounds_str = element.get_attribute('bounds')

        match = re.search(r'^\[(\d+),(\d+)\]\[(\d+),(\d+)\]$', bounds_str)

        start_point_x, start_point_y, end_point_x, end_point_y = _get_swipe_location(
            int(match.group(1)), int(match.group(2)), 
            int(match.group(3)), int(match.group(4)), 
            args['swipe_direction'])
        
    # 2、开始滑动
    args['session'].swipe(
        start_point_x, start_point_y, 
        end_point_x, end_point_y, 
        swipe_time = parseint_from_args(args, 'swipe_time'), 
        delay_after = parseint_from_args(args, 'delay_after'))
    
@visual_action
def press_key(**args) -> NoReturn:
    """
    {
        'session': session,
        'key': 'home'/'back'/'switch'/'enter',
        'delay_after': 1
    }
    """

    key = args['key']
    delay_after = parsefloat_from_args(args, 'delay_after', 1)

    if key == 'home':
        args['session'].home(delay_after=delay_after)
    elif key == 'back':
        args['session'].back(delay_after=delay_after)
    elif key == 'switch':
        args['session'].switchapp(delay_after=delay_after)
    elif key == 'enter':
        args['session'].enter(delay_after=delay_after)

@visual_action
def getoriention(**args) -> int:
    """
    {
        'session': session
    }
    """
    return args['session'].getoriention()

@visual_action
def setoriention(**args) -> NoReturn:
    """
    {
        'session': session,
        'oriention': 'horizontal'/'vertical'
    }
    """
    if args['oriention'] == 'horizontal':
        oriention = 1
    else:
        oriention = 0

    args['session'].setoriention(oriention)

@visual_action
def screenshot(**args):
    """
    {
        'session': session,
        'folder_path': '',
        'filename': 'xxx'
    }
    """

    args['session'].screenshot(args['folder_path'], filename=args['filename'])

@visual_action
def contains_element(**args) -> bool:
    """
    {
        'session': session,
        'content_type': 'contains_element/not_contains_element',
        'element': selector or element
    }
    """
    content_type = args["content_type"]
    element = args["element"]

    contains_result = args['session'].contains_element(element)

    if content_type == "contains_element":
        return contains_result
    elif content_type == "not_contains_element":
        return not contains_result
    else:
        raise ValueError(f"无效的检测内容类型{content_type}")


@visual_action
def click(**args) -> NoReturn:
    """
    {
        'session': session,
        'point_x': 1,
        'point_y': 3,
        'clicks': 'click'/'dbclick'/'longpress',
        'delay_after': 1
    }
    """

    point_x = parseint_from_args(args, 'point_x')
    point_y = parseint_from_args(args, 'point_y')
    clicks = args['clicks']
    delay_after = parseint_from_args(args, 'delay_after')

    if clicks == 'click':
        args['session'].click(point_x, point_y, delay_after = delay_after)
    elif clicks == 'dbclick':
        args['session'].dblclick(point_x, point_y, delay_after = delay_after)
    elif clicks == 'longpress':
        args['session'].longpress(point_x, point_y, delay_after = delay_after)


@visual_action
def get_clipboard_text(**args) -> str:
    return args['session'].get_clipboard_text()


@visual_action
def set_clipboard_text(**args) -> NoReturn:
    args['session'].set_clipboard_text(args['text'])


@visual_action
def push_file(**args) -> NoReturn:
    args['session'].push_file(args['file_path'], args['path_on_device'])


@visual_action
def pull_file(**args) -> NoReturn:
    args['session'].pull_file(args['path_on_device'], args['file_path'])



@visual_action
def get_session_detail(**args) -> dict:
    return args['session'].get_session_detail()


def _element(args, attribute_name='element') -> MobileElement:
    element = args.get(attribute_name, None)
    if element is None:
        return None
    elif isinstance(element, Selector):
        return args['session'].find(element)  # 如果是选择器，需要先转换为动态对象
    else:
        return element  # 如果是动态对象就直接返回

def _get_swipe_location(left, top, right, bottom, direction) -> tuple:
    width = right - left
    height = bottom - top
    if direction == 'up':
        return (left + 0.5*width, top + 0.75*height, left + 0.5*width, top + 0.25*height)
    elif direction == 'down':
        return (left + 0.5*width, top + 0.25*height, left + 0.5*width, top + 0.75*height)
    elif direction == 'left':
        return (left + 0.75*width, top + 0.5*height, left + 0.25*width, top + 0.5*height)
    elif direction == 'right':
        return (left + 0.25*width, top + 0.5*height, left + 0.75*width, top + 0.5*height)