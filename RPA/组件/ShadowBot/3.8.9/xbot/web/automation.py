'''
网页自动化模块
'''


from .._core import uidriver
from .._core.retry import Retry
from .._core.validation import valid, valid_multi, ValidPattern
from ..errors import UIAError, UIAErrorCode
from .browser import WebBrowser

from abc import ABCMeta, abstractmethod
from typing import NoReturn, List
import os


class WebAutomation(metaclass=ABCMeta):
    '''
    网页自动化模块
    '''

    def __init__(self, controller):
        self._controller = controller

    def create(self, url, *, load_timeout=20, stop_if_timeout=False, arguments=None) -> WebBrowser:
        """
        打开网页
        * @param url, 目标网址
        * @param load_timeout, 等待加载超时时间, 默认超时时间20s, 如果网页超时未加载完成则抛出`UIAError`异常
            * >0, 等待时间
            * 0, 不等待页面加载完成，立即返回
            * -1, 无限等待，直到页面加载完成
        * @param stop_if_timeout, 网页加载超时时是否停止加载网页, 默认是 `False` 不停止加载
        * @return `WebBrowser`, 返回打开的网页对象
        """

        valid('网址', url, ValidPattern.NotEmpty)
        valid_multi('页面加载超时时间', load_timeout, [
                    (ValidPattern.Type, int),
                    (ValidPattern.Min, -1)])
        bid = self._invoke('CreateBrowser', {
                           'url': url})
        browser = self._create_browser(bid)

        try:
            browser.wait_load_completed(load_timeout)
        except UIAError as e:
            if e.code == UIAErrorCode.Timeout and stop_if_timeout:
                browser.stop_load()
            else:
                raise e

        return browser

    def get(self, title=None, url=None, *, load_timeout=20, use_wildcard=False, stop_if_timeout=False) -> WebBrowser:
        """
        根据网址或标题获取网页, 默认模糊匹配, 如果`use_wildcard`为`True`则使用通配符方式匹配, 若匹配到多个网页,返回最新打开的网页
        * @param title, 标题
        * @param url, 网址
        * @param load_timeout, 等待加载超时时间, 默认超时时间20s, 如果网页超时未加载完成则抛出`UIAError`异常
            * >0, 等待时间
            * 0, 不等待页面加载完成，立即返回
            * -1, 无限等待，直到页面加载完成
        * @param use_wildcard, 是否使用通配符方式匹配, 默认为`False`
        * @param stop_if_timeout, 网页加载超时时是否停止加载网页, 默认是 `False` 不停止加载
        * @return `WebBrowser`, 返回获取到的网页对象
        """

        # title/class_name, 可以是字符串或通配符表达式('?' or '*')
        # 如果是字符串就模糊匹配
        if title is None and url is None:
            raise ValueError('网址或网页标题至少指定一个')

        for _ in Retry(5, interval=0.5, error_message='获取网页失败'):
            try:
                bid = self._invoke(
                    'GetBrowser', {'title': title, 'url': url, 'useWildcard': use_wildcard})
                browser = self._create_browser(bid)
                return browser
            except UIAError as e:
                if e.code == UIAErrorCode.NoSuchWindow:
                    pass
                else:
                    raise e
        try:
            browser.wait_load_completed(load_timeout)
        except UIAError as e:
            if e.code == UIAErrorCode.Timeout and stop_if_timeout:
                browser.stop_load()
            else:
                raise e

    def get_active(self, *, load_timeout=20, stop_if_timeout=False) -> WebBrowser:
        """
        获取当前选中或激活的网页
        * @param load_timeout, 等待加载超时时间, 默认超时时间20s, 如果网页超时未加载完成则抛出`UIAError`异常
        * @param stop_if_timeout, 网页加载超时时是否停止加载网页, 默认是 `False` 不停止加载
        * @return `WebBrowser`, 返回获取到的网页对象
        """

        bid = self._invoke('GetActiveBrowser')
        browser = self._create_browser(bid)

        try:
            browser.wait_load_completed(load_timeout)
        except UIAError as e:
            if e.code == UIAErrorCode.Timeout and stop_if_timeout:
                browser.stop_load()
            else:
                raise e

        return browser

    def get_all(self, *, title=None, url=None, use_wildcard=False) -> List[WebBrowser]:
        """
        获取已打开的网页对象列表, 默认获取所有网页, 可根据标题或网址筛选, 默认模糊匹配, 如果`'use_wildcard'`为`True`则使用通配符方式匹配
        * @param title, 标题, 支持模糊匹配,不填则匹配所有网页
        * @param url, 网址, 支持模糊匹配,不填则匹配所有网页
        * @param use_wildcard, 是否使用通配符方式匹配, 默认为`False`
        * @return `List[WebBrowser]`, 返回已打开的网页对象列表
        """

        bids = self._invoke('GetAllBrowsers', {'title': title, 'url': url, 'useWildcard': use_wildcard})
        return [self._create_browser(x) for x in bids]

    def get_cookies(self, url, *, name=None, domain=None, path=None) -> list:
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

        if url is None:
            raise ValueError('请指定要匹配的网址')        

        cookies = self._invoke('GetCookies',{'url': url, 'name': name, 'domain': domain, 'path': path})
        return cookies


    def close_all(self) -> NoReturn:
        """
        关闭全部已打开的网页
        """

        self._invoke('CloseAllBrowsers')

    def handle_save_dialog(self, dialog_result, file_folder, *, file_name=None, simulative=False, clipboard_input=True, wait_appear_timeout=20, send_key_delay=50, focus_timeout=1000) -> str:
        """
        处理网页下载对话框
        * @param file_folder, 文件保存路径
        * @param dialog_result, 点击下载对话框中按钮
            * `'ok'`, 确认下载, 
            * `'cancel'`, 取消下载
        * @param file_name, 保存文件名, 为None时自动为下载资源生成不重复的文件名
        * @param simulative, 模拟输入: 通过模拟人工的方式触发输入事件; 非模拟输入(自动化接口输入): 调用元素自身实现的自动化接口输入; 默认值为`True`
        * @param clipboard_input, 将输入路径和文件名添加到剪切板, 通过Ctrl+V的方式将内容填写到下载对话框的文件名输入框中,避免输入法问题
        * @param wait_appear_timeout, 等待对话框出现超时时间, 默认20s, 如果下载对话框超时未出现则抛出`UIAError`的异常
        * @param send_key_delay, 两次按键之间的时间间隔，默认为50ms
        * @param focus_timeout, 焦点超时时间(获取焦点和输入操作的间隔), 默认为1000ms
        """

        for _ in Retry(wait_appear_timeout, interval=0.5, error_message='等待对话框出现超时'):
            try:
                path = self._invoke('HandleSaveDialog', {
                    'dialogResult': dialog_result,
                    'fileFolder': file_folder,
                    'fileName': file_name,
                    'simulative': simulative,
                    'clipboardInput': clipboard_input,
                    "sendKeyDelay": send_key_delay,
                    'focusTimeout': focus_timeout})
                return path
            except UIAError as e:
                if e.code == UIAErrorCode.NoSuchWindow:
                    pass
                else:
                    raise e

    def handle_upload_dialog(self, dialog_result, filenames, *, simulative=False, clipboard_input=True, wait_appear_timeout=20, send_key_delay=50, focus_timeout=1000) -> NoReturn:
        """
        处理网页上传对话框
        * @param filenames, 要上传文件完整路径; 如果需要多文件上传, 输入完整路径数组，比如: ["C:\test.txt" "C:\text1.txt"]
        * @param dialog_result, 点击上传对话框中按钮 
            * `'ok'`, 确认上传
            * `'cancel'`, 取消上传
        * @param simulative, 模拟输入: 通过模拟人工的方式触发输入事件; 非模拟输入(自动化接口输入): 调用元素自身实现的自动化接口输入; 默认值为`True`
        * @param clipboard_input, 将输入路径和文件名添加到剪切板, 通过Ctrl+V的方式将内容填写到下载对话框的文件名输入框中,避免输入法问题
        * @param wait_appear_timeout, 等待上传对话框出现超时时间, 默认20s, 如果上传对话框超时未出现则抛出`UIAError`的异常
        * @param send_key_delay, 两次按键之间的时间间隔，默认为50ms
        * @param focus_timeout, 焦点超时时间(获取焦点和输入操作的间隔), 默认为1000ms
        """

        for _ in Retry(wait_appear_timeout, interval=0.5, error_message='等待对话框出现超时'):
            try:
                self._invoke('HandleUploadDialog', {
                             'dialogResult': dialog_result,
                             'filenames': filenames,
                             'simulative': simulative,
                             'clipboardInput': clipboard_input,
                             "sendKeyDelay": send_key_delay,
                             'focusTimeout': focus_timeout})
                break
            except UIAError as e:
                if e.code == UIAErrorCode.NoSuchWindow:
                    pass
                else:
                    raise e

    def before_file_dialog_open(self, scene='button', saveAs_file_folder=None, saveAs_file_name=None, choose_file_names=None):
        """
        上传、下载文件流程中，文件对话框打开之前调用，执行一些设置操作
        * @param scene, 下载场景，button/url
        * @param saveAs_file_folder，文件保存框-文件夹
        * @param saveAs_file_name，文件保存框-文件名
        * @param choose_file_names, 文件选择框-文件名列表
        """
        self._invoke('BeforeFileDialogOpen', {
            'scene': scene,
            'saveAsFileFolder': saveAs_file_folder,
            'saveAsFileName': saveAs_file_name,
            'chooseFileNames': choose_file_names
        })

    def after_file_dialog_closed(self):
        """
        上传、下载文件流程中，文件对话框打开之前调用，执行一些资源释放操作
        """
        self._invoke('AfterFileDialogClosed')

    def download_task_id(self) -> int:
        """
        获取下载任务id
        * @return `int`, 返回下载任务id
        """
        return self._invoke('GetDownloadTaskId')

    def is_download_complete(self, task_id) -> bool:
        """
        判断下载是否完成
        * @param task_id，下载任务id
        * @return `bool`, 返回下载完成结果
        """
        return self._invoke('IsDownloadComplete', {'taskId': task_id})

    def choose_file_dialog(self, filenames, *, simulative=False, clipboard_input=True, wait_appear_timeout=20, send_key_delay=50, focus_timeout=1000):
        self.handle_upload_dialog('ok', filenames,
                                  simulative=simulative,
                                  clipboard_input=clipboard_input,
                                  wait_appear_timeout=wait_appear_timeout,
                                  send_key_delay=send_key_delay,
                                  focus_timeout=focus_timeout
                                  )

    def saveAs_file_dialog(self, file_folder, *, file_name=None, simulative=False, clipboard_input=True, wait_appear_timeout=20, send_key_delay=50, focus_timeout=1000) -> str:
        return self.handle_save_dialog('ok',
                                       file_folder,
                                       file_name=file_name,
                                       simulative=simulative,
                                       clipboard_input=clipboard_input,
                                       wait_appear_timeout=wait_appear_timeout,
                                       send_key_delay=send_key_delay,
                                       focus_timeout=focus_timeout
                                       )

    def _invoke(self, action, args=None):
        return uidriver.execute(f'{self._controller}.{action}', args)

    @abstractmethod
    def _create_browser(self, bid) -> WebBrowser:
        pass
