from .._core import visual_action, parseint_from_args
from . import browser
from . import element
from xbot import web
from xbot.errors import UIAError, UIAErrorCode

import typing


@visual_action
def create(**args):
    """
    {
        'web_type': chrome/cef/ie
        'value': 'xxx'(url),
        'wait_load_completed': True
        'load_timeout': 20
        'stop_load_if_load_timeout': handleExcept/stopLoad
        'chrome_file_name': 'xxx'(folder)
        'ie_file_name': 'xxx'(folder)
        'arguments': --xxx
    }
    """
    # 参数处理
    web_type = args.get('web_type', 'cef')
    wait_load_completed = args.get('wait_load_completed', False)
    timeout = parseint_from_args(args, 'load_timeout')
    stop_if_timeout = args.get(
        'stop_load_if_load_timeout', 'handleExcept') == 'stopLoad'
    chrome_file_name = args.get('chrome_file_name', None)
    ie_file_name = args.get('ie_file_name', None)
    arguments = args.get('arguments', None)

    web.chrome.executable_path = chrome_file_name
    web.ie.executable_path = ie_file_name
    timeout = 0 if not wait_load_completed else timeout

    browser = web.create(args['value'], mode=web_type, load_timeout=timeout,
                         stop_if_timeout=stop_if_timeout, arguments=arguments)

    return browser


@visual_action
def get(**args):
    """
    {
        'web_type': chrome/cef/ie
        'mode': 'url/title/activated',
        'value': 'xxx',
        'wait_load_completed': True
        'load_timeout': 20,
        'stop_load_if_load_timeout': handleExcept/stopLoad
        'use_wildcard': True/False
    }
    """
    web_type = args.get('web_type', 'cef')
    timeout = parseint_from_args(args, 'load_timeout')
    model = args['mode']
    value = args['value']
    use_wildcard = args.get('use_wildcard', False)
    stop_if_timeout = args.get(
        'stop_load_if_load_timeout', 'handleExcept') == 'stopLoad'
    wait_load_completed = args['wait_load_completed']
    timeout = 0 if not wait_load_completed else timeout

    if model == 'url':
        browser = web.get(None, value, web_type, load_timeout=timeout,
                          use_wildcard=use_wildcard, stop_if_timeout=stop_if_timeout)
    elif model == 'title':
        browser = web.get(value, None, web_type, load_timeout=timeout,
                          use_wildcard=use_wildcard, stop_if_timeout=stop_if_timeout)
    else:
        browser = web.get_active(
            web_type, load_timeout=timeout, stop_if_timeout=stop_if_timeout)
    return browser


@visual_action
def get_all(**args):
    """
    {
        'web_type': chrome/cef/ie
        'mode': 'all/url/title',
        'value': 'xxx',
        'use_wildcard': True/False
    }
    """
    web_type = args['web_type']
    model = args['mode']
    value = args['value']
    use_wildcard = args.get('use_wildcard', False)

    if model == 'all':
        browser = web.get_all(web_type, title=None,
                              url=None, use_wildcard=use_wildcard)
    elif model == 'url':
        browser = web.get_all(web_type, title=None,
                              url=value, use_wildcard=use_wildcard)
    else:  # title
        browser = web.get_all(web_type, title=value,
                              url=None, use_wildcard=use_wildcard)
    return browser


@visual_action
def get_cookies(**args):
    """
    {
        'url_type': auto/manual,
        'browser': browser,
        'web_type': chrome/cef/ie
        'url': 'xxx',
        'name': 'xxx',
        'domain': 'xxx',
        'path': 'xxx',
    }
    """
    url_type = args.get('url_type', 'auto')
    browser = args['browser']
    web_type = args.get('web_type', 'cef')
    url = args['url']
    name = args['name']
    domain = args['domain']
    path = args['path']

    if url_type == 'auto':  # url_type和url网页对象自带
        return browser.get_cookies(name=name, domain=domain, path=path)
    else:  # manual
        return web.get_cookies(url, mode=web_type, name=name, domain=domain, path=path)


@visual_action
def handle_save_dialog(**args):
    """
    {
        'web_type': chrome/cef/ie
        'dialog_result': 'OK/Cancel',
        'file_folder': 'xxx',
        'file_name':  'xx.tt',

        'simulate': False
        'clipboard_input': False,

        'wait_appear_timeout': 20,
        'force_ime_ENG': False,
        'send_key_delay': 50
        'focus_timeout': 1000
    }
    """
    # 参数处理
    web_type = args.get('web_type', 'cef')
    dialog_result = args['dialog_result']
    if dialog_result == 'Cancle':
        dialog_result = 'cancel'
    file_folder = args.get('file_folder', None)
    file_name = args.get('file_name', None)

    simulative = args.get('simulate', False)
    clipboard_input = args.get('clipboard_input', True)

    timeout = parseint_from_args(args, 'wait_appear_timeout', 20)
    force_ime_ENG = args.get('force_ime_ENG', False)
    send_key_delay = parseint_from_args(args, 'send_key_delay', 50)
    focus_timeout = parseint_from_args(args, 'focus_timeout', 1000)

    # 方法调用
    return web.handle_save_dialog(file_folder,
                                  dialog_result,
                                  web_type,
                                  file_name=file_name,
                                  simulative=simulative,
                                  clipboard_input=clipboard_input,
                                  wait_appear_timeout=timeout,
                                  force_ime_ENG=force_ime_ENG,
                                  send_key_delay=send_key_delay,
                                  focus_timeout=focus_timeout)


@visual_action
def handle_upload_dialog(**args):
    """
    {
        'web_type': chrome/cef/ie
        'dialog_result': 'ok/cancel',
        'filename': 'xxx',

        'simulate': False,
        'clipboard_input': False,

        'wait_appear_timeout': 20，
        'force_ime_ENG': False,
        'send_key_delay': 50,
        'focus_timeout': 1000
    }
    """
    # 参数处理
    web_type = args.get('web_type', 'cef')
    dialog_result = args.get('dialog_result', 'OK')
    filenames = args['filename']
    if not isinstance(filenames, list):  # 兼容单个路径的情况
        filenames = [filenames]

    simulative = args.get('simulate', False)
    clipboard_input = args.get('clipboard_input', True)

    timeout = parseint_from_args(args, 'wait_appear_timeout', 20)
    force_ime_ENG = args.get('force_ime_ENG', False)
    send_key_delay = parseint_from_args(args, 'send_key_delay', 50)
    focus_timeout = parseint_from_args(args, 'focus_timeout', 1000)
    
    # 方法调用
    web.handle_upload_dialog(filenames,
                             dialog_result,
                             web_type,
                             simulative=simulative,
                             clipboard_input=clipboard_input,
                             wait_appear_timeout=timeout,
                             force_ime_ENG=force_ime_ENG,
                             send_key_delay=send_key_delay,
                             focus_timeout=focus_timeout)
