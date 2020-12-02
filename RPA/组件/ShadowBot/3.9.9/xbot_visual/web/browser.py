from .._core import visual_action, parseint_from_args, parsefloat_from_args
from xbot import web
from .element import _element
from xbot.errors import UIAError, UIAErrorCode
from xbot.selector import Selector
from xbot.app import logging

import typing


@visual_action
def close(**args):
    """
    {
        'operation': 'close_specified/close_all',
        'browser': browser,
        'web_type': chrome/cef/ie
        'task_kill': true/false
    }
    """
    # 参数处理
    web_type = args.get('web_type', 'cef')
    task_kill = args.get('task_kill',False)

    if args['operation'] == 'close_specified':
        _browser(args).close()
    else:
        web.close_all(web_type, task_kill=task_kill)


@visual_action
def navigate(**args):
    """
    {
        'browser': browser,
        'mode': 'back/forward/url/reload',
        'url': 'xxx',
        'load_timeout': 20
    }
    """
    timeout = parseint_from_args(args, 'load_timeout')
    if args['mode'] == 'back':
        _browser(args).go_back(load_timeout=timeout)
    elif args['mode'] == 'forward':
        _browser(args).go_forward(load_timeout=timeout)
    elif args['mode'] == 'url':
        _browser(args).navigate(args['url'], load_timeout=timeout)
    else:  # reload
        _browser(args).reload(
            ignore_cache=args['ignore_cache'], load_timeout=timeout)


@visual_action
def get_details(**args):
    """
    {
        'browser': browser
        'operation': 'url'
    }
    """
    operation = args['operation']
    if operation == 'url':
        prop = _browser(args).get_url()
    elif operation == 'title':
        prop = _browser(args).get_title()
    elif operation == 'html':
        prop = _browser(args).get_html()
    elif operation == 'text':
        prop = _browser(args).get_text()
    else:
        prop = None
    return prop


@visual_action
def wait_load_completed(**args):
    """
    {
        'browser': browser,
        'timeout': 20
    }
    """
    timeout = parseint_from_args(args, 'timeout')
    _browser(args).wait_load_completed(timeout)


@visual_action
def stop_load(**args):
    """
    {
        'browser': browser
    }
    """
    _browser(args).stop_load()


@visual_action
def execute_javascript(**args):
    """
    {
        'browser': browser,
        'element': 'element_id',
        'argument': None,
        'code': '...'
    }
    """
    if args['argument'] is not None and not isinstance(args['argument'], str):
        raise ValueError('输入的参数类型必须为字符串类型')
    element = _element(args)
    if element is not None:
        js_result = element.execute_javascript(
            args['code'], argument=args['argument'])
    else:
        js_result = _browser(args).execute_javascript(
            args['code'], argument=args['argument'])
    return js_result


@visual_action
def scroll_to(**args):
    """
    {
        'browser': browser,
        'element': 'element_id',
        'location': 'point/bottom/top',
        'behavior': 'instant/smooth'
        'top': 0,
        'left': 0
    }
    """
    # def scroll_to(self, *, location=ScrollLocation.Point, behavior='instant', top=0, left=0) -> typing.NoReturn:
    # # location: point(滚动到指定位置top/left), bottom(滚动到底部), top(滚动到顶部)
    # # behavior：smooth(平滑滚动), instant(瞬间滚动)
    # self._invoke(
    #     'ScrollTo', {'location': location, 'behavior': behavior, 'top': top, 'left': left})
    left = 0
    top = 0
    location = args.get('location', 'bottom')
    if location == 'point':
        left = parseint_from_args(args, 'left')
        top = parseint_from_args(args, 'top')

    element = _element(args)
    if element is not None:
        element.scroll_to(location=location,
                          behavior=args['behavior'], left=left, top=top)
    else:
        _browser(args).scroll_to(location=location,
                                 behavior=args['behavior'], left=left, top=top)


@visual_action
def handle_javascript_dialog(**args):
    """
    {
        'browser': browser,
        'dialog_result': 'ok/cancel',
        'filename': 'xxx',
        'wait_appear_timeout': 20
    }
    """
    timeout = parseint_from_args(args, 'wait_appear_timeout')

    dialog_result = args.get('dialog_result', 'cancel')

    # 兼容历史缺陷
    if dialog_result == 'Cancle':
        dialog_result = 'cancel'

    _browser(args).handle_javascript_dialog(dialog_result,
                                            text=args['text'], wait_appear_timeout=timeout)


@visual_action
def get_javascript_dialog_text(**args):
    """
    {
        'browser': browser,
        'wait_appear_timeout': 20
    }
    """
    timeout = parseint_from_args(args, 'wait_appear_timeout')
    dialog_text = _browser(args).get_javascript_dialog_text(
        wait_appear_timeout=timeout)
    return dialog_text


@visual_action
def start_monitor_network(**args):
    """
    {
        'browser': browser
    }
    """
    _browser(args).start_monitor_network()


@visual_action
def stop_monitor_network(**args):
    """
    {
        'browser': browser
    }
    """
    _browser(args).stop_monitor_network()


@visual_action
def get_responses(**args):
    """
    {
        'url': url
        'use_wildcard': False
        'resource_type': xxx
    }
    """
    url = args['url']
    use_wildcard = args.get('use_wildcard', False)
    resource_type = args.get('resource_type', 'All')
    return _browser(args).get_responses(url=url, use_wildcard=use_wildcard, resource_type=resource_type)


@visual_action
def contains_element_or_text(**args) -> bool:
    """
    {
        'browser': browser,
        'content_type': 'contains_element/not_contains_element/contains_text/not_contains_text',
        'selector': selector or element,
        'text':''
    }
    """
    browser = _browser(args)
    content_type = args['content_type']

    def contains_selector_or_element(selector_or_element):
        if isinstance(selector_or_element, Selector):
            return browser.is_element_displayed(selector_or_element)
        elif isinstance(selector_or_element, web.element.WebElement):
            try:
                return selector_or_element.is_displayed()
            except UIAError as e:
                if e.code == UIAErrorCode.NoSuchElement or e.code == UIAErrorCode.NoSuchElementID:
                    return False
                else:
                    raise e
        else:
            raise ValueError('selector参数类型不正确')

    if content_type == 'contains_element':
        return contains_selector_or_element(args['selector'])
    elif content_type == 'not_contains_element':
        return not contains_selector_or_element(args['selector'])
    elif content_type == 'contains_text':
        return args['text'] in browser.get_text()
    elif content_type == 'not_contains_text':
        return args['text'] not in browser.get_text()
    else:
        raise ValueError(f'无效的检测内容类型{content_type}')


def element_display(**args):
    browser = _browser(args)
    content_type = args['content_type']
    selector = args['selector']

    result = browser.is_element_displayed(selector)
    if content_type == 'display':
        return result
    elif content_type == 'undisplay':
        return not result


def _browser(args):
    return args['browser']
