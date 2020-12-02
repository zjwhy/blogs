from .._core import visual_action, parseint_from_args, parsefloat_from_args, parsesudoku_from_args, Rectangle
from xbot.app import databook
from xbot.selector import Selector, TableSelector
from xbot.web.element import WebElement
import xbot.web

from xbot.errors import UIAError, UIAErrorCode
from xbot.app import logging

import typing
import time


@visual_action
def click(**args):
    """
    {
        'browser': browser,
        'element': element_id,
        'simulate': True,
        'clicks': 'click'/'dbclick'
        'button': MouseButton.Left,

        'keys': null
        'delay_after': 1,

        'sudoku_part':,
        'offset_x':,
        'offset_y':
    }
    """
    # 参数处理
    element = _element(args)
    simulative = args['simulate']
    clicks = args['clicks']
    button = args['button']
    keys = args.get('keys', 'none')
    keys = 'none' if keys == 'null' else keys
    delay_after = parsefloat_from_args(args, 'delay_after', 1)

    sudoku_part = parsesudoku_from_args(args, 'sudoku_part')
    offset_x = parseint_from_args(args, 'offset_x')
    offset_y = parseint_from_args(args, 'offset_y')

    if clicks == 'click':
        element.click(button=button, simulative=simulative,
                      keys=keys, delay_after=delay_after, anchor=(sudoku_part, offset_x, offset_y))
    else:
        element.dblclick(simulative=simulative, delay_after=delay_after,
                         anchor=(sudoku_part, offset_x, offset_y))


@visual_action
def drag_to(**args):
    """
        'browser': ,
        'element': ,
        'drag_way': 'default'/'targetElement',
        'target_element':
        'left': 0,
        'top': 0,
        'delay_after':

        'sudoku_part':,
        'offset_x':,
        'offset_y':

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
def hover(**args):
    """
    {
        'browser': browser,
        'element': 'element_id',
        'simulate': True,
        'delay_after':

        'sudoku_part':,
        'offset_x':,
        'offset_y':
    }
    """
    # 参数处理
    element = _element(args)
    simulative = args['simulate']
    delay_after = parsefloat_from_args(args, 'delay_after', 1)

    sudoku_part = parsesudoku_from_args(args, 'sudoku_part')
    offset_x = parseint_from_args(args, 'offset_x')
    offset_y = parseint_from_args(args, 'offset_y')

    # 方法调用
    element.hover(simulative=simulative, delay_after=delay_after,
                  anchor=(sudoku_part, offset_x, offset_y))


@visual_action
def check(**args):
    """
    {
        'browser': browser,
        'element': 'element_id',
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
        'browser': browser,
        'element': 'element_id',
        'mode': 'text/index',
        'value': 'xxx',
        'match_mode' : 'fuzzy/exact/regex'
        'delay_after':
    }
    """
    element = _element(args)
    delay_after = parsefloat_from_args(args, 'delay_after', 1)

    if args['mode'] == 'text':
        match_mode = args.get('match_mode', 'fuzzy')
        element.select(args['value'], mode=match_mode, delay_after=delay_after)
    else:
        index = parseint_from_args(args, 'value') - 1
        element.select_by_index(index, delay_after=delay_after)


@visual_action
def input(**args):
    """
    {
        'browser': browser,
        'element': element_id,
        'text': '',
        'append': False,

        'simulate': True,
        'save_to_clipboard': False,
        'contains_hotkey': False,
        'force_ime_ENG': False,

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
    append = args['append']

    simulative = args['simulate']
    save_to_clipboard = args.get('save_to_clipboard', False)
    contains_hotkey = args['contains_hotkey']
    force_ime_ENG = args.get('force_ime_ENG', False)

    send_key_delay = parseint_from_args(args, 'send_key_delay', 50)
    focus_timeout = parseint_from_args(args, 'focus_timeout', 1000)
    delay_after = parsefloat_from_args(args, 'delay_after', 1)

    sudoku_part = parsesudoku_from_args(args, 'sudoku_part')
    offset_x = parseint_from_args(args, 'offset_x')
    offset_y = parseint_from_args(args, 'offset_y')

    # 方法调用
    if not save_to_clipboard:
        element.input(text=text,
                      simulative=simulative,
                      append=append,
                      contains_hotkey=contains_hotkey,
                      force_ime_ENG=force_ime_ENG,
                      send_key_delay=send_key_delay,
                      focus_timeout=focus_timeout,
                      delay_after=delay_after,
                      anchor=(sudoku_part, offset_x, offset_y)
                      )
    else:
        element.clipboard_input(text=text,
                                append=append,
                                focus_timeout=focus_timeout,
                                delay_after=delay_after,
                                anchor=(sudoku_part, offset_x, offset_y)
                                )


@visual_action
def input_password(**args):
    """
    {
        'browser': browser,
        'element': element_id,
        'text': '',

        'simulate': True,

        'force_ime_ENG': False,
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

    force_ime_ENG = args.get('force_ime_ENG', False)
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
                      append=False,
                      delay_after=delay_after,
                      anchor=(sudoku_part, offset_x, offset_y),
                      force_ime_ENG=force_ime_ENG,
                      send_key_delay=send_key_delay,
                      focus_timeout=focus_timeout)
    else:
        element.clipboard_input(text,
                                delay_after=delay_after,
                                anchor=(sudoku_part, offset_x, offset_y),
                                focus_timeout=focus_timeout)


@visual_action
def get_details(**args) -> str:
    """
    {
        'browser': browser,
        'element': 'element_id',
        'operation': 'url'
        'attribute_name': 'xxx'
    }
    """
    element = _element(args)
    operation = args['operation']

    if operation == 'text':
        prop = element.get_text()
    elif operation == 'html':
        prop = element.get_html()
    elif operation == 'value':
        prop = element.get_value()
    elif operation == 'href':
        prop = element.get_attribute('href')
    elif operation == 'other':
        prop = element.get_attribute(args['attribute_name'])
    else:
        prop = None
    return prop

@visual_action
def get_bounding(**args):
    """
    {
        'browser': browser,
        'element': 'element_id',
        'to96dpi': True,
        'relative_to':screen/window
    }
    """
    element = _element(args)
    to96dpi = args['to96dpi']
    relative_to = args['relative_to']
    (x, y, width, height) = element.get_bounding(to96dpi=to96dpi, relative_to=relative_to)
    return Rectangle(x, y, x+width, y+height, int(x+width/2), int(y+height/2), width, height)

@visual_action
def get_element(**args) -> WebElement:
    """
    {
        'browser': browser,
        'select_type':'selector'/'css_selector'/'xpath_selector'
        'selector' 'xxx',
        'css_selector':'',
        'xpath_selector':'',
        'parent': 'xxx',
        'timeout': 20,
        'is_related_parent'：False
    }
    """
    #print (args['selector'].value)
    is_related_parent = args['is_related_parent']
    parent = args.get('parent', None)
    # 只有在 关联了父控件 && 父控件是一个WebElement 的情况下，才需要在WebElement中寻找
    if not (is_related_parent and isinstance(parent, WebElement)):
        parent = args['browser']
    timeout = parseint_from_args(args, 'timeout')

    # 2、定位方式
    select_type = args['select_type']
    if select_type == 'selector':
        if isinstance(args['selector'], Selector):  # 选择器对象
            return parent.find(args['selector'], timeout=timeout)
        else:
            return args['selector']  # 动态对象(直接返回，无需再找)
    elif select_type == 'css_selector':
        # CSS选择器字符串
        return parent.find_by_css(args['css_selector'], timeout=timeout)
    else:
        # xpath选择器字符串
        return parent.find_by_xpath(args['xpath_selector'], timeout=timeout)


@visual_action
def get_all_elements(**args) -> typing.List[WebElement]:
    """
    {
        'browser': browser,
        'select_type':'selector'/'css_selector'/'xpath_selector'
        'selector': 'xxx',
        'css_selector':'',
        'xpath_selector':'',
        'parent': 'xxx',
        'timeout': 20,
        'is_related_parent'：False
    }
    """
    # 1、预处理
    is_related_parent = args['is_related_parent']
    parent = args.get('parent', None)
    if not (is_related_parent and isinstance(parent, WebElement)):
        parent = args['browser']
    timeout = parseint_from_args(args, 'timeout')

    # 2、定位方式
    select_type = args['select_type']
    if select_type == 'selector':
        if isinstance(args['selector'], Selector):  # 选择器
            return parent.find_all(args['selector'], timeout=timeout)
        else:
            if not isinstance(args['selector'], (list, tuple)):  # 单个值的情况
                return [args['selector']]
            else:
                return args['selector']  # 动态对象
    elif select_type == 'css_selector':
        return parent.find_all_by_css(args['css_selector'], timeout=timeout)
    else:
        return parent.find_all_by_xpath(args['xpath_selector'], timeout=timeout)


@visual_action
def iter_all_elements(**args) -> typing.List[WebElement]:
    """
    {
        'browser': browser,
        'selector': 'xxx',
        'timeout': 20
    }
    """
    timeout = parseint_from_args(args, 'timeout')
    return args['browser'].find_all(args['selector'], timeout=timeout)


@visual_action
def set_value(**args):
    """
    {
        'browser': browser,
        'element': 'element_id',
        'value': 'xxx'
    }
    """
    element = _element(args)
    element.set_value(args['value'])


@visual_action
def set_attribute(**args):
    """
    {
        'browser': browser,
        'element': 'element_id',
        'attribute_name': 'xxx',
        'value': 'xxx'
    }
    """
    element = _element(args)
    element.set_attribute(args['attribute_name'], args['value'])


@visual_action
def screenshot(**args):
    """
    {
        'browser': browser,
        'capture_area':Element
        'element': 'element_id',
        'folder_path': 'xxx'
        'random_filename': false/true
        'filename': 'xxx'
        'save_to_clipboard':false/true,
        'width':'xxx',
        'height':'xxxx'
    }
    """
    element = _element(args)
    random = args['random_filename']
    filename = args['filename']
    capture_area = args.get('capture_area', 'Element')
    save_to_clipboard = args.get('save_to_clipboard', False)
    if capture_area in['ViewPort', 'Whole']:
        width = parseint_from_args(args, 'width')
        height = parseint_from_args(args, 'height')
        full_size = capture_area == 'Whole'
        if save_to_clipboard:
            args['browser'].screenshot_to_clipboard(
                full_size=full_size, width=width, height=height)
        else:
            args['browser'].screenshot(
                args['folder_path'], file_name=filename, full_size=full_size, width=width, height=height)
    else:
        if save_to_clipboard:  # save to clipboard
            element.screenshot_to_clipboard()
        elif random or (filename is None or filename == ''):  # use random
            element.screenshot(args['folder_path'])
        else:  # use custom
            element.screenshot(args['folder_path'], filename=filename)


@visual_action
def wait(**args) -> bool:
    """
    {
        'browser': browser,
        'element': 'webElement/selector',
        'state':'appear/disappear',
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
        return args['browser'].wait_appear(element, timeout)
    else:
        return args['browser'].wait_disappear(element, timeout)


@visual_action
def data_scraping(**args) -> typing.List[typing.List[str]]:
    """
    {
        'browser': browser,
        'table_element': 'element_id', // only selector
        'handle_pager': False,
        'max_page': 1,
        'page_interval': 2,
        'page_element': 'element_id',
        'simulate_click_page': True,
        'save_to_datasheet': True
    }
    """
    rows = []
    table_selector = args.get('table_element', None)
    if not args['handle_pager']:
        rows = args['browser'].extract_table(table_selector)
        if args['save_to_datasheet']:
            for row in rows:
                databook.append_row(row)
    else:
        max_page = parseint_from_args(args, 'max_page')
        page_interval = parseint_from_args(args, 'page_interval')
        for current_page in range(max_page):
            # 1、提取一页数据
            try:
                page_rows = args['browser'].extract_table(table_selector)
            except UIAError as e:
                if e.code == UIAErrorCode.Timeout:  # extract_table Retry超时,找到0个相似元素时:跳过当前页,点击下一页
                    page_rows = []
                else:
                    raise e
            rows.extend(page_rows)
            # 2、保存到数据表格
            if args['save_to_datasheet'] and page_rows:
                for row in page_rows:
                    databook.append_row(row)
            # 3.点击下一页按钮
            if current_page < max_page - 1:  # 爬取最后一页数据之后，就不需要再点击下一页按钮了
                # 3.1、点击分页按钮
                try:
                    page_element = _element(args, 'page_element')
                except UIAError as e:
                    if e.code == UIAErrorCode.NoSuchElement:
                        raise UIAError(
                            '未找到"下一页"控件', UIAErrorCode.NoSuchElement)
                    if e.code == UIAErrorCode.Common:
                        raise UIAError('匹配到多个"下一页"控件, 无法唯一定位',
                                       UIAErrorCode.NoSuchElement)
                page_element.click(simulative=args['simulate_click_page'])
                # 3.2、分页间隔时间
                time.sleep(page_interval)
    return rows


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
        'browser': browser,
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
def upload(**args):
    '''
    {
        'browser': browser,
        'element': element,
        'file_name': filename,

        'simulate': False,
        'clipboard_input': True,

        'wait_dialog_appear_timeout': 20
        'force_ime_ENG': False,
        'send_key_delay': 50,
        'focus_timeout' : 1000,
    }
    '''
    # 参数处理
    element = _element(args)
    file_names = args['file_name']

    simulative = args.get('simulate', False)
    clipboard_input = args.get('clipboard_input', True)

    dialog_timeout = parseint_from_args(args, 'wait_dialog_appear_timeout')
    force_ime_ENG = args.get('force_ime_ENG', False)
    send_key_delay = parseint_from_args(args, 'send_key_delay', 50)
    focus_timeout = parseint_from_args(args, 'focus_timeout', 1000)

    element.upload(file_names,
                   simulative=simulative,
                   clipboard_input=clipboard_input,
                   dialog_timeout=dialog_timeout,
                   force_ime_ENG=force_ime_ENG,
                   send_key_delay=send_key_delay,
                   focus_timeout=focus_timeout
                   )


@visual_action
def download(**args):
    '''
    {
        'browser': browser,
        'scene': Button/Url,
        'download_button': element,
        'download_url': url,
        'file_folder': file_folder,
        'use_custom_filename' : True/False,
        'file_name': file_name,

        'wait_complete' : True/False,
        'wait_complete_timeout' : 60,

        'simulate': False,
        'clipboard_input': True,

        'wait_dialog_appear_timeout': 20
        'force_ime_ENG': False,
        'send_key_delay': 50,
        'focus_timeout' : 1000,
    }
    '''
    # 参数处理
    scene = args['scene']

    file_folder = args['file_folder']
    file_name = args['file_name']
    use_custom_filename = args.get('use_custom_filename', False)
    if not use_custom_filename:
        file_name = ''

    wait_complete = args.get('wait_complete', False)
    if not wait_complete:
        wait_complete_timeout = -1
    else:
        wait_complete_timeout = parseint_from_args(
            args, 'wait_complete_timeout')

    simulative = args.get('simulate', False)
    clipboard_input = args.get('clipboard_input', True)

    dialog_timeout = parseint_from_args(args, 'wait_dialog_appear_timeout')
    force_ime_ENG = args.get('force_ime_ENG', False)
    send_key_delay = parseint_from_args(args, 'send_key_delay', 50)
    focus_timeout = parseint_from_args(args, 'focus_timeout', 1000)

    # 方法调用
    if scene == 'Button':
        element = _element(args, attribute_name="download_button")
        return element.download(file_folder,
                                file_name=file_name,
                                wait_complete=wait_complete,
                                wait_complete_timeout=wait_complete_timeout,
                                simulative=simulative,
                                clipboard_input=clipboard_input,
                                dialog_timeout=dialog_timeout,
                                force_ime_ENG=force_ime_ENG,
                                send_key_delay=send_key_delay,
                                focus_timeout=focus_timeout
                                )
    else:
        url = args['download_url']
        return args['browser'].dowload_url(url,
                                           file_folder,
                                           file_name=file_name,
                                           wait_complete=wait_complete,
                                           wait_complete_timeout=wait_complete_timeout,
                                           simulative=simulative,
                                           clipboard_input=clipboard_input,
                                           dialog_timeout=dialog_timeout,
                                           focus_timeout=focus_timeout,
                                           )


def _element(args, attribute_name='element') -> WebElement:
    element = args.get(attribute_name, None)
    if element is None:
        return None
    elif isinstance(element, Selector) or isinstance(element, TableSelector):
        return args['browser'].find(element)  # 如果是选择器，就根据选择器获取控件对象
    else:
        return element  # 如果控件对象就直接返回
