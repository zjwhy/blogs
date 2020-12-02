'''
Web处理模块，可用来创建Web对象、获取Web标题、url等信息，还可以处理网页上传/下载对话框
'''

from . import cookies, element
from .browser import WebBrowser
from .cef import CEFAutomation
from .chrome import ChromeAutomation
from .ie import IEAutomation
from .automation import WebAutomation
from .element import WebElement

from typing import NoReturn, List


def create(url, mode='cef', *, load_timeout=20, stop_if_timeout=False, arguments=None) -> WebBrowser:
    """
    打开网页
    * @param url, 目标网址
    * @param mode, 浏览器类型
        *`'cef'` 影刀浏览器,
        *`'chrome'` Google Chrome浏览器
        *`'ie'` Internet Explorer浏览器
    * @param load_timeout, 等待加载超时时间, 默认超时时间20s, 如果网页超时未加载完成则抛出`UIAError`异常
        * >0, 等待时间
        * 0, 不等待页面加载完成，立即返回
        * -1, 无限等待，直到页面加载完成
    * @param stop_if_timeout, 网页加载超时时是否停止加载网页, 默认是 `False` 不停止加载
    * @param arguments, 命令行参数,必须是Chrome支持的命令行，参数格式如: --incognito, 可为空,仅创建Chrome时可用
    * @return `WebBrowser`, 返回打开的网页对象
    """

    automation = _create_web_automation(mode)
    browser = automation.create(
        url, load_timeout=load_timeout, stop_if_timeout=stop_if_timeout, arguments=arguments)
    return browser


def get(title=None, url=None, mode='cef', *, load_timeout=20, use_wildcard=False, stop_if_timeout=False) -> WebBrowser:
    """
    根据网址或标题获取网页, 默认模糊匹配, 如果`'use_wildcard'`为`True`则使用通配符方式匹配, 若匹配到多个网页,返回最新打开的网页
    * @param title, 标题
    * @param url, 网址
    * @param mode, 浏览器类型
        *`'cef'` 影刀浏览器,
        *`'chrome'` Google Chrome浏览器
        *`'ie'` Internet Explorer浏览器
    * @param load_timeout, 等待加载超时时间, 默认超时时间20s, 如果网页超时未加载完成则抛出`UIAError`异常
        * >0, 等待时间
        * 0, 不等待页面加载完成，立即返回
        * -1, 无限等待，直到页面加载完成
    * @param use_wildcard, 是否使用通配符方式匹配, 默认为`False`
    * @param stop_if_timeout, 网页加载超时时是否停止加载网页, 默认是 `False` 不停止加载
    * @return `WebBrowser`, 返回获取到的网页对象
    """

    automation = _create_web_automation(mode)
    browser = automation.get(title, url, load_timeout=load_timeout,
                             use_wildcard=use_wildcard, stop_if_timeout=stop_if_timeout)
    return browser


def get_active(mode='cef', *, load_timeout=20, stop_if_timeout=False) -> WebBrowser:
    """
    获取当前选中或激活的网页
    * @param mode, 浏览器类型
        *`'cef'` 影刀浏览器,
        *`'chrome'` Google Chrome浏览器
        *`'ie'` Internet Explorer浏览器
    * @param load_timeout, 等待加载超时时间, 默认超时时间20s, 如果网页超时未加载完成则抛出`UIAError`异常
    * @param stop_if_timeout, 网页加载超时时是否停止加载网页, 默认是 `False` 不停止加载
    * @return `WebBrowser`, 返回获取到的网页对象
    """

    automation = _create_web_automation(mode)
    browser = automation.get_active(
        load_timeout=load_timeout, stop_if_timeout=stop_if_timeout)
    return browser

def get_all(mode='cef', *, title=None, url=None, use_wildcard=False) -> List[WebBrowser]:
    """
    获取已打开的网页对象列表, 默认获取所有网页, 可根据标题或网址筛选, 默认模糊匹配, 如果`'use_wildcard'`为`True`则使用通配符方式匹配
    * @param mode, 浏览器类型
        *`'cef'` 影刀浏览器,
        *`'chrome'` Google Chrome浏览器
        *`'ie'` Internet Explorer浏览器
    * @param title, 标题
    * @param url, 网址
    * @param use_wildcard, 是否使用通配符方式匹配, 默认为`False`
    * @return `List[WebBrowser]`, 返回已打开的网页对象列表
    """

    automation = _create_web_automation(mode)
    browsers= automation.get_all(title=title, url=url, use_wildcard=use_wildcard)
    return browsers

def get_cookies(url, mode='cef', *, name=None, domain=None, path=None) -> list:
    """
    获取浏览器Cookie信息
    * @param mode, 浏览器类型
        *`'cef'` 影刀浏览器,
        *`'chrome'` Google Chrome浏览器
        *`'ie'` Internet Explorer浏览器
    * @param url, 根据是否与给定的 URL比如 'https://www.winrobot360.com'匹配, 筛选浏览器cookie(url为必填项)
    * @param name, 根据是否与给定的 name匹配, 筛选cookie(值为空则忽略 name筛选条件)
    * @param domain, 根据是否完全与给定的 domain比如 '.winrobot360.com'匹配, 或是否是其的子域名, 筛选cookie(浏览器类型为IE或值为空则忽略 domain筛选条件)
    * @param path, 根据是否与给定的path比如 '/', 筛选cookie(浏览器类型为IE或值为空则忽略 path筛选条件)
    * @return `list[dict]`, 返回筛选到的cookie列表, 列表项键包括'domain'、'expirationDate'、'name'、'value'、'httpOnly'..., 集合中的值可以通过比如 item['value'] 的方式获取"
    """

    automation = _create_web_automation(mode)
    cookies= automation.get_cookies(url, name=name, domain=domain, path=path)
    return cookies


def close_all(mode='cef') -> NoReturn:
    """
    关闭所有网页
    * @param mode, 浏览器类型
        * `'cef'`, 影刀浏览器,
        * `'chrome'`, Google Chrome浏览器
        *`'ie'` Internet Explorer浏览器
    """

    automation = _create_web_automation(mode)
    automation.close_all()


def handle_save_dialog(file_folder, dialog_result='ok', mode='cef', *, file_name=None, simulative=False, clipboard_input=True, wait_appear_timeout=20, send_key_delay=50, focus_timeout=1000) -> NoReturn:
    """
    处理网页下载对话框
    * @param file_folder, 文件保存路径
    * @param dialog_result, 点击下载对话框中按钮 
        * `'ok'`, 确认下载
        * `'cancel'`, 取消下载
    * @param mode, 浏览器类型
        *`'cef'`, 影刀浏览器,
        *`'chrome'`, Google Chrome浏览器
        *`'ie'`, Internet Explorer浏览器
    * @param file_name, 保存文件名, 为None时, 使用下载资源默认文件名, 若无默认文件名则自动为下载资源生成不重复的文件名
    * @param simulative, 模拟输入: 通过模拟人工的方式触发输入事件; 非模拟输入(自动化接口输入): 调用元素自身实现的自动化接口输入; 默认值为`True`
    * @param clipboard_input, 是否使用剪切板输入文件路径
    * @param wait_appear_timeout, 等待对话框出现超时时间, 默认20s, 如果下载对话框超时未出现则抛出`UIAError`的异常
    * @param send_key_delay, 两次按键之间的时间间隔，默认为50ms
    * @param focus_timeout, 焦点超时时间(获取焦点和输入操作的间隔), 默认为1000ms
    """

    automation = _create_web_automation(mode)
    return automation.handle_save_dialog(dialog_result,
                                         file_folder,
                                         file_name=file_name,
                                         simulative=simulative,
                                         clipboard_input=clipboard_input,
                                         wait_appear_timeout=wait_appear_timeout,
                                         send_key_delay=send_key_delay,
                                         focus_timeout=focus_timeout)


def handle_upload_dialog(filenames, dialog_result='ok', mode='cef', *, simulative=False, clipboard_input=True, wait_appear_timeout=20, send_key_delay=50, focus_timeout=1000) -> NoReturn:
    """
    处理网页上传对话框
    * @param filenames, 要上传文件完整路径; 如果需要多文件上传, 在python模式下输入完整路径数组，比如: [r"C:\test.txt",r"C:\text1.txt"]
    * @param dialog_result, 点击上传对话框中按钮 
        * `'ok'`, 确认上传
        * `'cancel'`, 取消上传
    * @param mode, 浏览器类型
        *`'cef'`, 影刀浏览器,
        *`'chrome'`, Google Chrome浏览器
        *`'ie'`, Internet Explorer浏览器
    * @param simulative, 模拟输入: 通过模拟人工的方式触发输入事件; 非模拟输入(自动化接口输入): 调用元素自身实现的自动化接口输入; 默认值为`True`
    * @param clipboard_input, 剪切板输入: 将输入内容添加到剪切板通过Ctrl+V指令将内容填写到输入框避免输入法问题
    * @param wait_appear_timeout, 等待上传对话框出现超时时间, 默认20s, 如果上传对话框超时未出现则抛出`UIAError`的异常
    * @param send_key_delay, 两次按键之间的时间间隔，默认为50ms
    * @param focus_timeout, 焦点超时时间(获取焦点和输入操作的间隔), 默认为1000ms
    """
    if not isinstance(filenames, list):  # 兼容单个路径的情况
        filenames = [filenames]
    automation = _create_web_automation(mode)
    automation.handle_upload_dialog(
        dialog_result,
        filenames,
        simulative=simulative,
        clipboard_input=clipboard_input,
        wait_appear_timeout=wait_appear_timeout,
        send_key_delay=send_key_delay,
        focus_timeout=focus_timeout)


def _create_web_automation(mode) -> WebAutomation:
    if mode == None:
        raise ValueError(f'参数mode值无效, {mode}')
    lower_mode = mode.lower()

    if lower_mode == 'cef':
        return CEFAutomation()
    elif lower_mode == 'chrome':
        return ChromeAutomation()
    elif lower_mode == 'ie':
        return IEAutomation()
    else:
        raise ValueError(f'参数mode值无效, {mode}')
