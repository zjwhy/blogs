from .._core import visual_action, parseint_from_args, parsefloat_from_args
import typing

from xbot.mobile.element import MobileElement
from xbot.selector import Selector


@visual_action
def get_element(**args):
    """
    {
        'session': session,
        'select_type': 'xbot_selector'/'id'/'accessibility_id'/'label_name'/'xpath'/'uiautomator_selector'
        'xbot_selector': ,
        'str_selector': ''
    }
    """
    select_type = args['select_type']

    if select_type == 'xbot_selector':
        if isinstance(args['xbot_selector'], Selector):
            return args['session'].find(args['xbot_selector'])
        else:
            return selector
    elif select_type == 'id':
        return args['session'].find_by_id(args['str_selector'])
    elif select_type == 'accessibility_id':
        return args['session'].find_by_accessibility_id(args['str_selector'])
    elif select_type == 'label_name':
        return args['session'].find_by_label_name(args['str_selector'])
    elif select_type == 'xpath':
        return args['session'].find_by_xpath(args['str_selector'])
    elif select_type == 'uiautomator_selector':
        return args['session'].find_by_uiautomator_selector(args['str_selector'])

@visual_action
def get_all_elements(**args):
    """
    {
        'session': session,
        'select_type': 'xbot_selector'/'id'/'accessibility_id'/'label_name'/'xpath'/'uiautomator_selector'
        'xbot_selector': ,
        'str_selector': ''
    }
    """
    select_type = args['select_type']

    if select_type == 'xbot_selector':
        xbot_selector = args['xbot_selector']
        if isinstance(xbot_selector, Selector):
            return args['session'].find_all(xbot_selector)
        else:
            if not isinstance(xbot_selector, (list,tuple)):
                return [xbot_selector]
            else:
                return xbot_selector
    elif select_type == 'id':
        return args['session'].find_all_by_id(args['str_selector'])
    elif select_type == 'accessibility_id':
        return args['session'].find_all_by_accessibility_id(args['str_selector'])
    elif select_type == 'label_name':
        return args['session'].find_all_by_label_name(args['str_selector'])
    elif select_type == 'xpath':
        return args['session'].find_all_by_xpath(args['str_selector'])
    elif select_type == 'uiautomator_selector':
        return args['session'].find_all_by_uiautomator_selector(args['str_selector'])


@visual_action
def iter_all_elements(**args):
    """
    {
        'session': session,
        'selector': selector
    }
    """
    selector = args['selector']
    
    if isinstance(selector, Selector):
        return args['session'].find_all(selector)
    else:
        if not isinstance(selector,(list,tuple)):
            return [selector]
        else:
            return selector


@visual_action
def click(**args):
    """
    {
        'session': session,
        'element': element,
        'clicks': 'click'/'dbclick'/'longpress',
        'delay_after': 1
    }
    """
    element = _element(args)
    clicks = args['clicks']
    delay_after = parseint_from_args(args, 'delay_after')

    if clicks == 'click':
        element.click(delay_after = delay_after)
    elif clicks == 'dbclick':
        element.dblclick(delay_after = delay_after)
    elif clicks == 'longpress':
        element.longpress(delay_after = delay_after)


@visual_action
def input(**args):
    """
    {
        'session': session,
        'element': element,
        'text': 'xxx',
        'append': False/True,
        'delay_after': 1
    }
    """
    element = _element(args)
    delay_after = parsefloat_from_args(args, 'delay_after', 1)
    
    element.input(args['text'], append=args['append'], delay_after=delay_after)


@visual_action
def get_details(**args) -> str:
    """
    {
        'session': session,
        'element': element,
        'operation': 'text'/'attribute'
        'attribute_name': 'xxx'
    }
    """
    element = _element(args)
    operation = args['operation']

    if operation == 'text':
        prop = element.get_text()
    elif operation == 'other':
        prop = element.get_attribute(args['attribute_name'])
    else:
        prop = None
    return prop


@visual_action
def screenshot(**args):
    """
    {
        'session': session,
        'element': element,
        'folder_path': '',
        'random_filename': false/true,
        'filename': 'xxx'
    }
    """
    element = _element(args)

    if args['random_filename'] == True:
        element.screenshot(args['folder_path'])
    else:
        element.screenshot(args['folder_path'], filename=args['filename'])


def _element(args, attribute_name='element') -> MobileElement:
    element = args.get(attribute_name, None)
    if element is None:
        return None
    elif isinstance(element, Selector):
        return args['session'].find(element)  # 如果是选择器，需要先转换为动态对象
    else:
        return element  # 如果是动态对象就直接返回