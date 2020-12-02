import os
import ctypes
from .._core import visual_action, parseint_from_args, parsefloat_from_args, _expand_path
from xbot import win32
from xbot_visual.win32 import window, element
from xbot.win32 import clipboard

import typing


@visual_action
def minimize_all() -> typing.NoReturn:
    win32.minimize_all()


@visual_action
def move_mouse(**args) -> typing.NoReturn:
    """
        'point_x':,
        'point_y':,
        'relative_to': 'screen'/'currentactivatedwindow'/'currentmouseposition',
        'move_speed': 'instant'/'fast'/'middle'/'slow',
        'delay_after':
    """
    point_x = parseint_from_args(args, 'point_x')
    point_y = parseint_from_args(args, 'point_y')
    delay_after = parsefloat_from_args(args, 'delay_after', 1)

    # MouseMoveSpeed
    move_speed = args.get('move_speed', 'instant')

    # RelativeToMode
    relative_to = args.get('relative_to', 'screen')

    if relative_to == 'currentactivatedwindow':
        relative_to = 'window'
    elif relative_to == 'currentmouseposition':
        relative_to = 'position'

    win32.mouse_move(point_x=point_x, point_y=point_y,  relative_to=relative_to,
                     move_speed=move_speed, delay_after=delay_after)


@visual_action
def send_keys(**args) -> typing.NoReturn:
    """
        'keys':'',
        'hardware_driver_input': False
        'delay_after':,
        'send_key_delay':
    """
    keys = args['keys']
    hardware_driver_input = args.get('hardware_driver_input', False)
    delay_after = parsefloat_from_args(args, 'delay_after', 1)
    send_key_delay = parseint_from_args(args, 'send_key_delay', 50)

    win32.send_keys(keys=keys, send_key_delay=send_key_delay, hardware_driver_input=hardware_driver_input, delay_after=delay_after)


@visual_action
def click_mouse(**args) -> typing.NoReturn:
    """
        'is_move_mouse_before_click':True/False,
        'point_x':,
        'point_y':,
        'relative_to': 'screen'/'currentactivatedwindow'/'currentmouseposition',
        'move_speed': 'instant'/'fast'/'middle'/'slow',
        'button':'left'/'right'/'middle'
        'click_type':'click'/'dbclick'/'down'/'up',
        'hardware_driver_click': False
        'keys': 'null',
        'delay_after':,
    """

    # 1、移动鼠标
    if args['is_move_mouse_before_click'] == True:
        # 1.1、目标位置
        point_x = parseint_from_args(args, 'point_x')
        point_y = parseint_from_args(args, 'point_y')

        # 1.2、移速
        move_speed = args.get('move_speed', 'instant')

        # 1.3、相对于
        relative_to = args.get('relative_to', 'screen')

        if relative_to == 'currentactivatedwindow':
            relative_to = 'window'
        elif relative_to == 'currentmouseposition':
            relative_to = 'position'

        # 1.4、...
        win32.mouse_move(point_x=point_x, point_y=point_y,
                         relative_to=relative_to, move_speed=move_speed, delay_after=1)

    # 2、点击鼠标
    # 2.1、鼠标按钮
    button = args.get('button', 'left')

    # 2.2、键盘的辅助按钮
    keys = args.get('keys', 'none')
    keys = 'none' if keys == 'null' else keys

    # 2.3、点击类型
    click_type = args.get('click_type', 'click')

    # 2.4、是否使用驱动点击
    hardware_driver_click = args.get('hardware_driver_click', False)

    # 2.4、...
    delay_after = parsefloat_from_args(args, 'delay_after', 1)
    win32.mouse_click(button=button,
                      click_type=click_type,
                     hardware_driver_click=hardware_driver_click,
                      keys=keys,
                      delay_after=delay_after)


@visual_action
def wheel_mouse(**args) -> typing.NoReturn:
    """
        'wheel_direction': 'up'/'down',
        'wheel_times': 1,
        'keys': 'null',
        'delay_after':
    """
    delay_after = parsefloat_from_args(args, 'delay_after', 1)

    # 1、滚动方向
    wheel_direction = args.get('wheel_direction', 'up')

    # 2、滚动次数
    wheel_times = parseint_from_args(args, 'wheel_times')

    # 3、键盘辅助按键
    keys = args.get('keys', 'none')
    keys = 'none' if keys == 'null' else keys

    # 4、
    win32.mouse_wheel(wheel_direction=wheel_direction,
                      wheel_times=wheel_times, keys=keys, delay_after=delay_after)


@visual_action
def get_mouse_position(**args) -> tuple:
    """
        'relative_to': 'screen'/'currentactivatedwindow',
    """
    relative_to = args.get('relative_to', 'screen')

    if relative_to == 'currentactivatedwindow':
        relative_to = 'window'

    return win32.get_mouse_position(relative_to=relative_to)


@visual_action
def clipboard_get_text() -> str:
    return clipboard.get_text()


@visual_action
def clipboard_set_text(**args):
    clipboard.set_text(args['text'])


@visual_action
def clipboard_clear():
    clipboard.clear()


@visual_action
def clipboard_set_file(**args):
    file_path = args['file_path']
    clipboard.set_file([_expand_path(file_path)])


@visual_action
def lock_screen(**args):
    win32.lock_screen()
    

@visual_action
def unlock_screen(**args):
    user_name = args['user_name']
    password = args['password']

    win32.unlock_screen(user_name, password)
    

@visual_action
def set_ime(**args):
    lang = args['lang']
    win32.set_ime(lang)


@visual_action
def get_ime(**args):
    return win32.get_ime()


@visual_action
def get_selected_text(**args) -> str:
    wait_time = parseint_from_args(args, 'wait_time', 0)
    return win32.get_selected_text(wait_time)