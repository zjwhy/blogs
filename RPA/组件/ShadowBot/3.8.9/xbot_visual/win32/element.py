from .._core import visual_action, parseint_from_args, parsefloat_from_args, parsesudoku_from_args
from xbot.selector import Selector
from xbot.win32.element import Win32Element
from xbot.win32.window import Win32Window


import typing
import time


@visual_action
def get_element(**args):
    """
    {
        'window': ,
        'selector' ,
        'timeout': 20,
    }
    """
    selector = args['selector']
    timeout = parseint_from_args(args, 'timeout')
    if isinstance(selector, Selector):
        return args['window'].find(selector, timeout=timeout)
    else:
        return selector


@visual_action
def get_all_elements(**args):
    """
    {
        'window': ,
        'selector': ,
        'timeout': 20,
    }
    """
    selector = args['selector']
    timeout = parseint_from_args(args, 'timeout')
    if isinstance(selector, Selector):
        return args['window'].find_all(selector, timeout=timeout)
    else:
        if not isinstance(selector, (list, tuple)):
            return [selector]
        else:
            return selector


@visual_action
def iter_all_elements(**args):
    """
    {
        'window': win32Window,
        'selector': selector or tableSelector,
        'timeout': 20
    }
    """
    timeout = parseint_from_args(args, 'timeout')
    return args['window'].find_all(args['selector'], timeout=timeout)


@visual_action
def click(**args):
    """
    {
        'window': ,
        'element': ,
        'clicks': 'click'/'dbclick'
        'button': MouseButton.Left,

        'keys': null,
        'delay_after': 1,

        'sudoku_part': middleCenter,
        'offset_x': 0,
        'offset_y': 0,

        'simulate': True,
        'move_mouse':True
    }
    """
    # 参数处理
    element = _element(args)
    clicks = args['clicks']
    button = args.get('button', 'left')

    keys = args.get('keys', 'none')
    keys = 'none' if keys == 'null' else keys
    delay_after = parsefloat_from_args(args, 'delay_after', 1)

    sudoku_part = parsesudoku_from_args(args, 'sudoku_part')
    offset_x = parseint_from_args(args, 'offset_x')
    offset_y = parseint_from_args(args, 'offset_y')

    simulative = args['simulate']
    move_mouse = args['move_mouse']

    # 方法调用
    if clicks == 'click':
        element.click(button=button, simulative=simulative, keys=keys, delay_after=delay_after, move_mouse=move_mouse,
                      anchor=(sudoku_part, offset_x, offset_y)
                      )
    else:
        element.dblclick(simulative=simulative, delay_after=delay_after, move_mouse=move_mouse,
                         anchor=(sudoku_part, offset_x, offset_y)
                         )


@visual_action
def input(**args):
    """
    {
        'window': window,
        'element': element_id,
        'text': 'xxx',
        'append': False,

        'simulate': True,
        'save_to_clipboard': False,
        'contains_hotkey': False,

        'send_key_delay': 50
        'focus_timeout': 1000
        'delay_after': 1,

        'sudoku_part': middleCenter,
        'offset_x': 0,
        'offset_y': 0
    }
    """
    # 参数处理
    element = _element(args)
    text = args['text']
    append = args['append']

    simulative = args['simulate']
    save_to_clipboard = args.get('save_to_clipboard', False)
    contains_hotkey = args['contains_hotkey']

    send_key_delay = parseint_from_args(args, 'send_key_delay', 50)
    focus_timeout = parseint_from_args(args, 'focus_timeout', 1000)
    delay_after = parsefloat_from_args(args, 'delay_after', 1)

    sudoku_part = parsesudoku_from_args(args, 'sudoku_part')
    offset_x = parseint_from_args(args, 'offset_x')
    offset_y = parseint_from_args(args, 'offset_y')

    # 方法调用
    if not save_to_clipboard:
        element.input(text,
                      simulative=simulative,
                      append=append,
                      contains_hotkey=contains_hotkey,
                      send_key_delay=send_key_delay,
                      focus_timeout=focus_timeout,
                      delay_after=delay_after,
                      anchor=(sudoku_part, offset_x, offset_y)
                      )
    else:
        element.clipboard_input(text,
                                append=append,
                                focus_timeout=focus_timeout,
                                delay_after=delay_after,
                                anchor=(sudoku_part, offset_x, offset_y)
                                )


@visual_action
def hover(**args):
    """
    {
        'window': window,
        'element': ,
        'delay_after':

        'sudoku_part':,
        'offset_x':,
        'offset_y':
    }
    """
    # 参数处理
    element = _element(args)
    delay_after = parsefloat_from_args(args, 'delay_after', 1)

    sudoku_part = parsesudoku_from_args(args, 'sudoku_part')
    offset_x = parseint_from_args(args, 'offset_x')
    offset_y = parseint_from_args(args, 'offset_y')

    # 方法调用
    element.hover(delay_after=delay_after, anchor=(
        sudoku_part, offset_x, offset_y))


@visual_action
def check(**args):
    """
    {
        'window': window,
        'element': ,
        'mode': 'check',
        'delay_after':
    }
    """
    mode = args.get('mode', 'check')

    element = _element(args)
    delay_after = parsefloat_from_args(args, 'delay_after', 1)

    element.check(mode, delay_after=delay_after)


@visual_action
def select(**args):
    """
    {
        'window': window,
        'element': '',
        'mode': 'text/index',
        'value': 'xxx',
        'delay_after':
    }
    """
    element = _element(args)
    delay_after = parsefloat_from_args(args, 'delay_after', 1)

    if args['mode'] == 'text':
        element.select(args['value'], delay_after=delay_after)
    else:
        index = parseint_from_args(args, 'value') - 1
        element.select_by_index(index, delay_after=delay_after)


@visual_action
def input_password(**args):
    """
    {
        'window': window,
        'element': element_id,
        'text': '',

        'simulate': True,
        'save_to_clipboard': False,

        'send_key_delay': 50,
        'focus_timeout': 1000,
        'delay_after': 1,

        'sudoku_part': middleCenter,
        'offset_x': 0,
        'offset_y': 0
    }
    """
    # 参数处理
    element = _element(args)
    text = args['text']

    simulative = args['simulate']
    save_to_clipboard = args.get('save_to_clipboard', False)

    send_key_delay = parseint_from_args(args, 'send_key_delay', 50)
    focus_timeout = parseint_from_args(args, 'focus_timeout', 1000)
    delay_after = parsefloat_from_args(args, 'delay_after', 1)

    offset_x = parseint_from_args(args, 'offset_x')
    offset_y = parseint_from_args(args, 'offset_y')
    sudoku_part = parsesudoku_from_args(args, 'sudoku_part')

    # 方法调用
    if not save_to_clipboard:
        element.input(text,
                      simulative=simulative,
                      append=False,
                      delay_after=delay_after,
                      anchor=(sudoku_part, offset_x, offset_y),
                      send_key_delay=send_key_delay,
                      focus_timeout=focus_timeout)
    else:
        element.clipboard_input(text,
                                delay_after=delay_after,
                                anchor=(sudoku_part, offset_x, offset_y),
                                focus_timeout=focus_timeout)


@visual_action
def set_value(**args):
    """
    {
        'window': window,
        'element': '',
        'value': 'xxx'
    }
    """
    element = _element(args)
    element.set_value(args['value'])


@visual_action
def get_details(**args):
    """
    {
        'window': window,
        'element': '',
        'operation': ''
        'attribute_name': ''
    }
    """
    element = _element(args)
    operation = args['operation']

    if operation == 'text':
        prop = element.get_text()
    elif operation == 'value':
        prop = element.get_value()
    elif operation == 'other':
        prop = element.get_attribute(args['attribute_name'])
    else:
        prop = None
    return prop


@visual_action
def wait(**args):
    """
    {
        'window': window,
        'element': 'win32Element/selector',
        'state':'appear/disappear'
        'iswait':True/False,
        'timeout': 20
    }
    """
    # 1、预处理
    state = args['state']
    timeout = parseint_from_args(args, 'timeout')
    element = args['element']
    if element is None:
        raise ValueError('element参数类型不正确')
    if not state in ['appear', 'disappear']:
        raise ValueError('state参数类型不正确')
    if not args['iswait']:
        timeout = -1  # 无限等待

    # 2、等待出现/消失
    if state == 'appear':
        return args['window'].wait_appear(element, timeout)
    else:
        return args['window'].wait_disappear(element, timeout)


@visual_action
def drag_to(**args):
    """
        'window': ,
        'element': ,
        'drag_way': 'default'/'targetElement',
        'target_element':
        'left': 0,
        'top': 0,

        'delay_after': 1,

        'sudoku_part': middleCenter,
        'offset_x': 0,
        'offset_y': 0

        'release_sudoku_part':,
        'release_offset_x':,
        'release_offset_y':
    """
    # 鼠标按下位置
    element = _element(args)
    press_sudoku_part = parsesudoku_from_args(args, 'sudoku_part')
    press_offset_x = parseint_from_args(args, 'offset_x')
    press_offset_y = parseint_from_args(args, 'offset_y')
    (press_anchor_position_x, press_anchor_position_y) = element.get_anchor_position(
        anchor=(press_sudoku_part, press_offset_x, press_offset_y))

    # 获取鼠标横(left)纵(top)向位移, 鼠标释放位置锚点要在这里提前计算, 在C#侧不好处理
    if args['drag_way'] == 'targetElement':
        target_element = _element(args, 'target_element')
        # 鼠标释放位置
        release_sudoku_part = parsesudoku_from_args(
            args, 'release_sudoku_part')
        release_offset_x = parseint_from_args(args, 'release_offset_x')
        release_offset_y = parseint_from_args(args, 'release_offset_y')
        (release_anchor_position_x, release_anchor_position_y) = target_element.get_anchor_position(
            anchor=(release_sudoku_part, release_offset_x, release_offset_y))

        left = release_anchor_position_x - press_anchor_position_x
        top = release_anchor_position_y - press_anchor_position_y
    else:
        left = parseint_from_args(args, 'left') - press_anchor_position_x
        top = parseint_from_args(args, 'top') - press_anchor_position_y

    delay_after = parsefloat_from_args(args, 'delay_after', 1)

    # 方法调用
    element.drag_to(simulative=True, top=top, left=left,
                    delay_after=delay_after, anchor=(press_sudoku_part, press_offset_x, press_offset_y))


@visual_action
def screenshot(**args):
    """
    {
        'window': window,
        'element': '',
        'folder_path': 'xxx'
        'random_filename': false/true
        'filename': 'xxx'
        'save_to_clipboard':'fale/true'
    }
    """
    element = _element(args)
    random = args['random_filename']
    filename = args['filename']
    save_to_clipboard = args.get('save_to_clipboard', False)

    if save_to_clipboard:
        element.screenshot_to_clipboard()  # save to clipboard
    elif random or (filename is None or filename == ''):  # use random
        element.screenshot(args['folder_path'])
    else:  # use custom
        element.screenshot(args['folder_path'], filename=filename)


@visual_action
def get_select_item(**args):
    element = _element(args)
    get_way = args['get_way']
    if get_way == 'selected':
        return element.get_selected_item()
    elif get_way == 'select_all':
        return element.get_all_select_items()


@visual_action
def get_associated_elements(**args):
    '''
    {
        'window': window,
        'element': '',
        'associated_kind': 'parent'/'child'/'sibling'
        'child_access_kind': 'all'/'index',
        'child_index': 0,
        'sibling_direction': 'next'/'previous'
    }
    '''
    element = _element(args)
    if args['associated_kind'] == 'parent':
        return element.parent()
    elif args['associated_kind'] == 'sibling':
        if args['sibling_direction'] == 'next':
            return element.next_sibling()
        else:
            raise ValueError('暂不支持获取上一个相邻元素')
    elif args['associated_kind'] == 'child':
        if args['child_access_kind'] == 'all':
            return element.children()
        elif args['child_access_kind'] == 'index':
            child_index = parseint_from_args(args, 'child_index')
            return element.child_at(child_index)


@visual_action
def expand_tree_and_select_node(**args):
    """
    {
        'window': window,
        'element': '',
        'text_path': 'xxx/yyy/zzz'
    }
    """
    element = _element(args)
    element.expand_tree_and_select_node(args['text_path'])


@visual_action
def get_table_row_count(**args):
    element = _element(args)
    return element.get_table_row_count()


@visual_action
def get_table_column_count(**args):
    element = _element(args)
    return element.get_table_column_count()


@visual_action
def get_table_cell_by_rownum_and_columnnum(**args):
    element = _element(args)
    row_num = parseint_from_args(args, 'row_num')
    column_num = parseint_from_args(args, 'column_num')
    return element.get_table_cell_by_rownum_and_columnnum(row_num, column_num)


def _element(args, attribute_name='element') -> Win32Element:
    element = args.get(attribute_name, None)
    if element is None:
        return None
    elif isinstance(element, Selector):
        return args['window'].find(element)  # 如果是选择器，需要先在窗口中找一下
    else:
        return element  # 如果是Win32Element对象就直接返回
