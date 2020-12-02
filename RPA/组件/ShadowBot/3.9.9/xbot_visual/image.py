from xbot.win32 import image
from ._core import visual_action, parseint_from_args, parsesudoku_from_args


@visual_action
def wait(**args) -> bool:
    """
    {
        'window_kind':'screen'/'currentactivatewindow',
        'wait_mode':'appear'/'disappear',
        'template_images':
        'is_wait_all_images':True/False,
        'iswait':True/False,
        'timeout':20
    }
    """
    # 1、预处理
    wait_mode = args['wait_mode']
    image_selectors = args['template_images']
    wait_all = args['is_wait_all_images']

    timeout = parseint_from_args(args, 'timeout')
    if not args['iswait']:
        timeout = -1  # 无限等待

    # 2、等待出现/消失
    if wait_mode == 'appear':
        if args['window_kind'] == 'screen':
            return image.wait_appear(image_selectors, wait_all=wait_all, timeout=timeout)
        else:
            return image.wait_appear_from_window(0, image_selectors, wait_all=wait_all, timeout=timeout)
    else:
        if args['window_kind'] == 'screen':
            return image.wait_disappear(image_selectors, wait_all=wait_all, timeout=timeout)
        else:
            return image.wait_disappear_from_window(0, image_selectors, wait_all=wait_all, timeout=timeout)
    
@visual_action
def hover(**args):
    """
    {
        'window_kind':'screen'/'currentactivatewindow',
        'template_images':
        'sudoku_part':,
        'offset_x':,
        'offset_y':,
        'timeout':5,
        'delay_after':1
    }
    """
    image_selectors = args['template_images']
    offset_x = parseint_from_args(args, 'offset_x')
    offset_y = parseint_from_args(args, 'offset_y')
    sudoku_part = parsesudoku_from_args(args, 'sudoku_part')
    timeout = parseint_from_args(args, 'timeout', 0)                            # 对于可视化来说，和原来的逻辑（没有重试超时机制）保持一致
    delay_after = parseint_from_args(args, 'delay_after', 0)                    # 对于可视化来说，和原来的逻辑（执行后无延迟）保持一致

    if sudoku_part is None:
        sudoku_part = 'middleCenter'
    if args['window_kind'] == 'screen':
        image.hover(image_selectors, anchor=(sudoku_part, offset_x, offset_y), timeout=timeout, delay_after=delay_after)
    else:
        image.hover_on_window(0, image_selectors, anchor=(sudoku_part, offset_x, offset_y), timeout=timeout, delay_after=delay_after)

@visual_action
def click(**args):
    """
    {
        'window_kind':'screen'/'currentactivatewindow',
        'template_images':
        'sudoku_part':,
        'offset_x':,
        'offset_y':,

        'clicks': 'click'/'dbclick'
        'button': MouseButton.Left,
        'keys': 'null',
        'move_mouse':True/False,
        'timeout':5,
        'delay_after':1
    }
    """
    image_selectors = args['template_images']
    offset_x = parseint_from_args(args, 'offset_x')
    offset_y = parseint_from_args(args, 'offset_y')
    sudoku_part = parsesudoku_from_args(args, 'sudoku_part')

    if sudoku_part is None:
        sudoku_part = 'middleCenter'

    clicks = args['clicks']
    move_mouse = args['move_mouse']
    keys = args.get('keys', 'none')
    keys = 'none' if keys == 'null' else keys
    timeout = parseint_from_args(args, 'timeout', 0)                       # 对于可视化来说，和原来的逻辑（没有重试超时机制）保持一致
    delay_after = parseint_from_args(args, 'delay_after', 0)               # 对于可视化来说，和原来的逻辑（执行后无延迟）保持一致

    # 1、单击
    if clicks == 'click':       
        if args['window_kind'] == 'screen':
            image.click(image_selectors, anchor=(sudoku_part, offset_x, offset_y), 
                                                button=args['button'], keys=keys, move_mouse=move_mouse, timeout=timeout, delay_after=delay_after)
        else:
            image.click_on_window(0, image_selectors, anchor=(sudoku_part, offset_x, offset_y), 
                                                    button=args['button'], keys=keys, move_mouse=move_mouse, timeout=timeout, delay_after=delay_after)
    # 2、双击
    else:
        if args['window_kind'] == 'screen':
            image.dblclick(image_selectors, anchor=(sudoku_part, offset_x, offset_y), move_mouse=move_mouse, timeout=timeout, delay_after=delay_after)
        else:
            image.dblclick_on_window(0, image_selectors, anchor=(sudoku_part, offset_x, offset_y), move_mouse=move_mouse, timeout=timeout, delay_after=delay_after)

@visual_action
def exist(**args):
    """
    {
        'window_kind':'screen'/'currentactivatewindow',
        'exist_mode':'exist'/'notexist',
        'template_images':
        'is_find_all_images':True/False
    }
    """
    image_selectors = args['template_images']
    find_all = args['is_find_all_images']

    if args['exist_mode'] == 'exist':
        if args['window_kind'] == 'screen':
            return image.wait_appear(image_selectors, wait_all=find_all, timeout=0)
        else:
            return image.wait_appear_from_window(0, image_selectors, wait_all=find_all, timeout=0)
    else:
        if args['window_kind'] == 'screen':
            return image.wait_disappear(image_selectors, wait_all=find_all, timeout=0)
        else:
            return image.wait_disappear_from_window(0, image_selectors, wait_all=find_all, timeout=0)
