from .element import WebElement
from .._core import uidriver
from .._core.retry import Retry
from .._core.validation import valid, valid_multi, ValidPattern
from ..selector import Selector, TableSelector, _get_selector_by_name
from .cookies import Cookies
from ..errors import UIAError, UIAErrorCode

from abc import ABCMeta, abstractmethod
from typing import NoReturn, Any, List
import time


class WebBrowser(metaclass=ABCMeta):
    '''
    浏览器自动化模块
    '''

    def __init__(self, controller, bid):
        self._controller = controller
        self._cookies = Cookies(controller)
        self.bid = bid

    def get_url(self) -> str:
        '''
        获取网址
        * @return `str`, 返回网页地址
        '''

        return self._invoke('GetUrl')

    def get_title(self) -> str:
        '''
        获取网页标题
        * @return `str`, 返回网页标题
        '''

        return self._invoke('GetTitle')

    def get_text(self) -> str:
        '''
        获取网页文本内容
        * @return `str`, 返回网页内容
        '''

        return self._invoke('GetText')

    def get_html(self) -> str:
        '''
        获取网页html
        * @return `str`, 返回网页HTML内容
        '''

        return self._invoke('GetHtml')

    def get_cookies(self, *, name=None, domain=None, path=None) -> list:
        '''
        获取网页Cookie信息
        * @param name, 根据是否与给定的 name匹配, 筛选cookie(值为空则忽略 name筛选条件)
        * @param domain, 根据是否完全与给定的 domain比如 '.winrobot360.com'匹配, 或是否是其的子域名, 筛选cookie(浏览器类型为IE或值为空则忽略 domain筛选条件)
        * @param path, 根据是否与给定的path比如 '/', 筛选cookie(浏览器类型为IE或值为空则忽略 path筛选条件)
        * @return `list[dict]`, 返回筛选到的cookie列表, 列表项键包括'domain'、'expirationDate'、'name'、'value'、'httpOnly'..., 集合中的值可以通过比如 item['value'] 的方式获取"
       '''

        cookies = self._invoke('GetCookies',{'name': name, 'domain': domain, 'path': path})
        return cookies

    def activate(self) -> NoReturn:
        '''
        激活网页
        '''

        self._invoke('Activate')

    def navigate(self, url, *, load_timeout=20) -> NoReturn:
        '''
        跳转至新网址
        * @param url, 新网页地址
        * @param load_timeout, 等待加载超时时间, 默认超时时间20s, 如果网页超时未加载完成则抛出`UIAError`异常
        '''

        self._invoke('Navigate', {'url': url})
        if load_timeout != 0:
            time.sleep(0.5)  # 防止浏览器尚未加载新页面
            self.wait_load_completed(load_timeout)

    def go_back(self, *, load_timeout=20) -> NoReturn:
        '''
        网页回退
        * @param load_timeout, 等待加载超时时间, 默认超时时间20s, 如果网页超时未加载完成则抛出`UIAError`异常
        '''

        self._invoke('GoBack')
        if load_timeout != 0:
            time.sleep(0.5)  # 防止浏览器尚未加载新页面
            self.wait_load_completed(load_timeout)

    def go_forward(self, *, load_timeout=20) -> NoReturn:
        '''
        网页前进
        * @param load_timeout, 等待加载超时时间, 默认超时时间20s, 如果网页超时未加载完成则抛出`UIAError`异常
        '''

        self._invoke('GoForward')
        if load_timeout != 0:
            time.sleep(0.5)  # 防止浏览器尚未加载新页面
            self.wait_load_completed(load_timeout)

    def reload(self, ignore_cache=False, *, load_timeout=20) -> NoReturn:
        '''
        网页重新加载
        * @param ignore_cache, 是否忽略缓存，默认不忽略
        * @param load_timeout, 等待加载超时时间, 默认超时时间20s, 如果网页超时未加载完成则抛出`UIAError`异常
        '''

        self._invoke('Reload', {'ignoreCache': ignore_cache})
        if load_timeout != 0:
            self.wait_load_completed(load_timeout)

    def stop_load(self) -> NoReturn:
        '''
        网页停止加载
        '''

        self._invoke('StopLoad')

    def is_load_completed(self) -> bool:
        '''
        判断网页是否加载完成
        * @param `bool`, 返回网页是否加载完成, 完成返回`True`, 否则返回`False`
        '''

        return self._invoke('IsLoadCompleted')

    def wait_load_completed(self, timeout=20) -> NoReturn:
        '''
        等待网页加载完成
        * @timeout, 等待加载超时时间, 默认超时时间20s, 如果网页超时未加载完成则抛出`UIAError`异常
        '''

        valid_multi('timeout', timeout, [
                    (ValidPattern.Type, int),
                    (ValidPattern.Min, -1)])
        for _ in Retry(timeout, interval=0.5, error_message='等待页面加载超时'):
            if self.is_load_completed():
                break

    def close(self) -> NoReturn:
        '''
        关闭网页
        '''

        self._invoke('Close')

    def execute_javascript(self, code, argument=None) -> Any:
        '''
        执行Javascript脚本
        * @param code, 要执行的JS脚本，必须为javascript函数形式，如:
        ```python
        """
        function (element, args) {
            // element为null
            // args表示输入的参数
            return args;
        }
        """
        ```
        * @param argument, 要传入到JS函数中的参数，必须为字符串，如果需要传入其他类型可以先将其转为JSON字符串形式
        * @return `Any`, 返回JS脚本执行结果
        '''

        # js执行异常，这里会抛出UIAError
        return self._invoke('ExecuteJavaScript', {'argument': argument, 'code': code})

    # 暂时不提供异步方法，可以通过settimeout模拟出来
    # def execute_javascript_async(self, code) -> NoReturn:
    #     # js执行异常时不会抛出异常
    #     return self._invoke('ExecuteJavaScriptAsync', {'code': code})

    def scroll_to(self, *, location='bottom', behavior='instant', top=0, left=0) -> NoReturn:
        '''
        鼠标滚动网页
        * @param location, 网页要滚动到的位置, 默认滚动到底部
            *`'bottom'` 滚动到底部
            *`'top'`, 滚动到顶部
            *`'point'`, 滚动到指定位置
        * @param behavior, 网页滚动效果, 默认瞬间滚动
            *`'instant'`, 瞬间滚动
            *`'smooth'`, 平滑滚动
        * @param top, 滚动到指定位置的纵坐标
        * @param left, 滚动到指定位置的横坐标
        '''

        # location: point(滚动到指定位置top/left), bottom(滚动到底部), top(滚动到顶部)
        # behavior：smooth(平滑滚动), instant(瞬间滚动)
        self._invoke(
            'ScrollTo', {'location': location, 'behavior': behavior, 'top': top, 'left': left})

    def handle_javascript_dialog(self, dialog_result='ok', *, text=None, wait_appear_timeout=20) -> NoReturn:
        '''
        处理网页对话框
        * @param dialog_result, 网页对话框处理方式
            *`'ok'`, 确定,
            *`'cancel'`, 取消
        * @param text, 输入网页对话框的内容, 可为None
        * @param wait_appear_timeout, 等待网页对话框出现, 默认超时时间20s, 如果网页超时未加载完成则抛出`UIAError`异常
        '''

        for _ in Retry(wait_appear_timeout, interval=0.5, error_message='等待对话框出现超时'):
            try:
                self._invoke('HandleJavascriptDialog', {
                             'dialogResult': dialog_result, 'text': text})
                break
            except UIAError as e:
                if e.code == UIAErrorCode.NoSuchWindow:
                    pass
                else:
                    raise e

    def get_javascript_dialog_text(self, *, wait_appear_timeout=20) -> str:
        '''
        获取网页对话框内容
        * @param wait_appear_timeout, 等待网页对话框出现, 默认超时时间20s, 如果网页超时未加载完成则抛出`UIAError`异常
        * @return `str`, 返回网页对话框的内容
        '''

        for _ in Retry(wait_appear_timeout, interval=0.5, error_message='等待对话框出现超时'):
            try:
                return self._invoke('GetJavascriptDialogText')
            except UIAError as e:
                if e.code == UIAErrorCode.NoSuchWindow:
                    pass
                else:
                    raise e

    def start_monitor_network(self) -> NoReturn:
        '''
        开始监听网页请求
        '''
        self._invoke('StartMonitorNetWork')

    def stop_monitor_network(self) -> NoReturn:
        '''
        停止监听网页请求
        '''
        self._invoke('StopMonitorNetWork')

    def get_responses(self, *, url=None, use_wildcard=False, resource_type='All') -> list:
        """
        根据输入的资源路径Url,筛选网页请求结果,列表项键包括'url'、type'、'body'、'base64Encoded', 集合中的值可以通过比如 item['body'] 的方式获取
        * @param url, 资源路径Url
        * @param use_wildcard, 是否使用通配符方式匹配, 默认为`False`模糊匹配, 如果为`True`则使用通配符方式匹配
        * @param resource_type, 要过滤的网页请求结果类型, 包括
            * All, XHR, Script, Stylesheet, Image, Media, Font, Document
            * WebSocket, Manifest, TextTrack, Fetch, EventSource, Other
        * @return `list[dict]`, 返回获取到的网页请求结果列表, 列表项键包括'url'、'type'、'body'、'base64Encoded',集合中的值可以通过比如 item['body'] 的方式获取"
        """
        return self._invoke('GetResponses', {'url': url, 'useWildcard': use_wildcard, 'resourceType': resource_type})

    def wait_appear(self, selector_or_element, timeout=20) -> bool:
        '''
        等待元素出现
        * @param selector_or_element, 要等待的目标元素, 支持以下格式: 
            * 选择器名称, `str`类型
            * 选择器对象, `Selector`类型
            * Web元素对象, `WebElement`类型
        * @param timeout, 等待网页元素出现超时时间, 默认超时时间20s
        * @return `bool`, 返回网页元素是否出现, 出现返回`True`, 否则返回`False`
        '''
        if isinstance(selector_or_element, str):
            selector_or_element = _get_selector_by_name(selector_or_element)

        if isinstance(selector_or_element, Selector):
            for _ in Retry(timeout, interval=0.5, ignore_exception=True):
                try:
                    element_id_list = self._invoke(
                        'QuerySelectorAll', {'selector': selector_or_element.value})
                    if len(element_id_list) == 0:
                        continue
                    elif len(element_id_list) > 1:
                        raise UIAError('匹配到多个控件, 无法唯一定位', UIAErrorCode.Common)
                    else:
                        element = self._create_element(
                            self.bid, element_id_list[0])
                        if not element.is_displayed():
                            continue
                        else:
                            return True
                except UIAError as e:
                    if e.code == UIAErrorCode.PageIsLoading or e.code == UIAErrorCode.NoSuchWindow \
                            or e.code == UIAErrorCode.NoSuchElement or e.code == UIAErrorCode.NoSuchElementID:
                        pass
                    else:
                        break
            return False
        elif isinstance(selector_or_element, WebElement):
            for _ in Retry(timeout, interval=0.5, ignore_exception=True):
                try:
                    if not selector_or_element.is_displayed():
                        continue
                    else:
                        return True
                except UIAError as e:
                    if e.code == UIAErrorCode.PageIsLoading or e.code == UIAErrorCode.NoSuchWindow \
                            or e.code == UIAErrorCode.NoSuchElement or e.code == UIAErrorCode.NoSuchElementID:
                        pass
                    else:
                        break
            return False
        else:
            raise ValueError('selector_or_element参数类型不正确')

    def wait_disappear(self, selector_or_element, timeout=20) -> bool:
        '''
        等待元素消失
        * @param selector_or_element, 要等待的目标元素, 支持以下格式: 
            * 选择器名称, `str`类型
            * 选择器对象, `Selector`类型
            * Web元素对象, `WebElement`类型
        * @param timeout, 等待网页元素消失超时时间, 默认超时时间20s
        * @return `bool`, 返回网页元素是否消失的结果, 消失返回`True`, 否则返回`False`
        '''
        if isinstance(selector_or_element, str):
            selector_or_element = _get_selector_by_name(selector_or_element)

        if isinstance(selector_or_element, Selector):
            for _ in Retry(timeout, interval=0.5, ignore_exception=True):
                try:
                    element_id_list = self._invoke(
                        'QuerySelectorAll', {'selector': selector_or_element.value})
                    if len(element_id_list) == 0:
                        return True
                    elif len(element_id_list) > 1:
                        raise UIAError('匹配到多个控件, 无法唯一定位', UIAErrorCode.Common)
                    else:
                        element = self._create_element(
                            self.bid, element_id_list[0])
                        if not element.is_displayed():
                            return True
                        else:
                            continue
                except UIAError as e:
                    if e.code == UIAErrorCode.PageIsLoading or e.code == UIAErrorCode.NoSuchWindow \
                            or e.code == UIAErrorCode.NoSuchElement or e.code == UIAErrorCode.NoSuchElementID:
                        pass
                    else:
                        break
            return False
        elif isinstance(selector_or_element, WebElement):
            for _ in Retry(timeout, interval=0.5, ignore_exception=True):
                try:
                    if not selector_or_element.is_displayed():
                        return True
                    else:
                        continue
                except UIAError as e:
                    if e.code == UIAErrorCode.PageIsLoading or e.code == UIAErrorCode.NoSuchWindow:
                        pass
                    elif e.code == UIAErrorCode.NoSuchElement or e.code == UIAErrorCode.NoSuchElementID:
                        return True
                    else:
                        break
            return False
        else:
            raise ValueError('selector_or_element参数类型不正确')

    def find_all(self, selector, *, timeout=20) -> List[WebElement]:
        '''
        在当前网页中获取与选择器匹配的相似网页元素列表, 如果没有相似元素则返回一个空列表
        * @param selector, 要查找的选择器, 支持以下格式: 
            * 选择器名称, `str`类型
            * 选择器对象, `Selector`类型
        * @param timeout, 获取网页相似元素列表超时时间, 默认超时时间20s
        * @return `List[WebElement]`, 返回和目标元素相似网页元素列表
        '''
        if isinstance(selector, str):
            selector = _get_selector_by_name(selector)

        if not isinstance(selector, Selector):
            raise ValueError('selector参数类型不正确')
        for _ in Retry(timeout, interval=0.5, ignore_exception=True):
            try:
                element_id_list = self._invoke(
                    'QuerySelectorAll', {'selector': selector.value})
                if len(element_id_list) == 0:
                    continue
                return [self._create_element(self.bid, x) for x in element_id_list]
            except UIAError as e:
                if e.code == UIAErrorCode.PageIsLoading or e.code == UIAErrorCode.NoSuchWindow \
                        or e.code == UIAErrorCode.NoSuchElement or e.code == UIAErrorCode.NoSuchElementID:
                    pass
                else:
                    raise e
        return []

    def find_all_by_css(self, css_selector, *, timeout=20) -> List[WebElement]:
        '''
        在当前网页中获取符合CSS选择器的网页元素列表, 如果没有相似元素则返回一个空列表
        * @param css_selector, CSS选择器 (`str`)
        * @param timeout, 获取网页相似元素列表超时时间, 默认超时时间20s
        * @return `List[WebElement]`, 返回相似网页元素列表
        '''

        for _ in Retry(timeout, interval=0.5, ignore_exception=True):
            try:
                element_id_list = self._invoke('QueryCSSSelectorAll', {
                                               'cssSelector': css_selector})
                if len(element_id_list) == 0:
                    continue
                return [self._create_element(self.bid, x) for x in element_id_list]
            except UIAError as e:
                if e.code == UIAErrorCode.PageIsLoading or e.code == UIAErrorCode.NoSuchWindow \
                        or e.code == UIAErrorCode.NoSuchElement or e.code == UIAErrorCode.NoSuchElementID:
                    pass
                else:
                    raise e
        return []

    def find_all_by_xpath(self, xpath_selector, *, timeout=20) -> List[WebElement]:
        '''
        在当前网页中获取符合Xpath选择器的网页元素列表, 如果没有相似元素则返回一个空列表
        * @param xpath_selector, Xpath选择器 (`str`)
        * @param timeout, 获取网页相似元素列表超时时间, 默认超时时间20s, 
        * @return `List[WebElement]`, 返回相似网页元素列表
        '''

        for _ in Retry(timeout, interval=0.5, ignore_exception=True):
            try:
                element_id_list = self._invoke('QueryXPathSelectorAll', {
                                               'xpathSelector': xpath_selector})
                if len(element_id_list) == 0:
                    continue
                return [self._create_element(self.bid, x) for x in element_id_list]
            except UIAError as e:
                if e.code == UIAErrorCode.PageIsLoading or e.code == UIAErrorCode.NoSuchWindow \
                        or e.code == UIAErrorCode.NoSuchElement or e.code == UIAErrorCode.NoSuchElementID:
                    pass
                else:
                    raise e
        return []

    def find(self, selector, *, timeout=20) -> WebElement:
        '''
        在当前网页中获取与选择器匹配的网页元素对象, 如果找到多个或者未找到相似控件则抛出 `UIAError` 异常
        * @param selector, 要查找的选择器, 支持以下格式: 
            * 选择器名称, `str`类型
            * 选择器对象, `Selector`类型
        * @param timeout, 获取目标网页元素对象超时时间, 默认超时时间20s
        * @return `WebElement`, 返回目标网页元素对象
        '''
        if isinstance(selector, str):
            selector = _get_selector_by_name(selector)

        elements = self.find_all(selector, timeout=timeout)
        if len(elements) == 0:
            raise UIAError('未找到控件', UIAErrorCode.NoSuchElement)
        elif len(elements) > 1:
            raise UIAError('匹配到多个控件, 无法唯一定位', UIAErrorCode.Common)
        else:
            return elements[0]

    def find_by_css(self, css_selector, *, timeout=20) -> WebElement:
        '''
        在当前网页中获取符合CSS选择器的网页元素对象, 如果找到多个或者未找到相似控件则抛出 `UIAError` 异常
        * @param css_selector, CSS选择器 (`str`)
        * @param timeout, 以CSS选择器获取网页元素对象超时时间, 默认超时时间20s
        * @return `WebElement`, 返回网页元素对象
        '''

        elements = self.find_all_by_css(css_selector, timeout=timeout)
        if len(elements) == 0:
            raise UIAError('未找到控件', UIAErrorCode.NoSuchElement)
        elif len(elements) > 1:
            raise UIAError('匹配到多个控件, 无法唯一定位', UIAErrorCode.Common)
        else:
            return elements[0]

    def find_by_xpath(self, xpath_selector, *, timeout=20) -> WebElement:
        '''
        在当前网页中获取符合Xpath选择器的网页元素对象, 如果找到多个或者未找到相似控件则抛出 `UIAError` 异常
        * @param xpath_selector, Xpath选择器 (`str`)
        * @param timeout, 以Xpath选择器获取网页元素对象超时时间, 默认超时时间20s
        * @return `WebElement`, 返回网页元素对象
        '''

        elements = self.find_all_by_xpath(xpath_selector, timeout=timeout)
        if len(elements) == 0:
            raise UIAError('未找到控件', UIAErrorCode.NoSuchElement)
        elif len(elements) > 1:
            raise UIAError('匹配到多个控件, 无法唯一定位', UIAErrorCode.Common)
        else:
            return elements[0]

    def is_element_displayed(self, selector) -> bool:  # 判断元素在用户层面上的的可见性
        '''
        网页元素是否可见
        * @param selector, 要查找的选择器, 支持以下格式: 
            * 选择器名称, `str`类型
            * 选择器对象, `Selector`类型
            * 动态元素, `WebElement`类型
        * @return `bool`, 返回网页元素是否可见, 可见返回`True`, 不可见返回 `False` 
        '''
        if isinstance(selector, str): # 选择器名称
            selector = _get_selector_by_name(selector)
        
        if isinstance(selector, Selector): # 选择器对象
            try:
                element_id_list = self._invoke(
                    'QuerySelectorAll', {'selector': selector.value})
                if len(element_id_list) == 0:
                    return False
                elif len(element_id_list) > 1:
                    raise UIAError('匹配到多个控件, 无法唯一定位', UIAErrorCode.Common)
                else:
                    element = self._create_element(self.bid, element_id_list[0])
            except UIAError as e:
                if e.code == UIAErrorCode.PageIsLoading or e.code == UIAErrorCode.NoSuchWindow \
                        or e.code == UIAErrorCode.NoSuchElement or e.code == UIAErrorCode.NoSuchElementID:
                    return False
                else:
                    raise e
        elif isinstance(selector, WebElement): # 动态元素
            element = selector
        else:
            raise ValueError('selector参数类型不正确')
        
        return element.is_displayed()

    def extract_table(self, table_selector, *, timeout=20) -> List[List[str]]:
        '''
        获取选择器对应表格数据
        * @param table_selector, 表格选择器, 支持以下格式:
            * 选择器名称, `str`类型
            * 选择器对象, `TableSelector`类型
        * @param timeout, 在网页上查找和目标元素相似的元素列表超时时间, 默认超时时间20s
        * @return `list`, 返回网页上与目标元素相似的元素列表
        '''
        if isinstance(table_selector, str):
            table_selector = _get_selector_by_name(table_selector)

        if not isinstance(table_selector, TableSelector):
            raise ValueError('selector参数类型不正确')
        for _ in Retry(timeout, interval=0.5, error_message='未找到控件'):
            try:
                # 处理抓取整个数据表格的情况
                if len(table_selector.value['base']) > 0 and len(table_selector.value['columns']) == 0:
                    elementId = self._invoke(
                        'QueryBaseTableSelector', {'selector': table_selector.value})
                    element = self._create_element(self.bid, elementId)
                    args = {'browserId': self.bid, 'elementId': elementId}
                    rows = uidriver.execute(
                        f'{element._controller}.GetBaseTableValue', args)
                else:
                    rows = self._invoke('QueryTableSelector', {
                        'selector': table_selector.value})
                return rows
            except UIAError as e:
                if e.code == UIAErrorCode.PageIsLoading or e.code == UIAErrorCode.NoSuchWindow or e.code == UIAErrorCode.NoSuchElement:
                    pass
                else:
                    raise e

    def dowload_url(self, url, file_folder, *, file_name=None, wait_complete=False, wait_complete_timeout=60,  simulative=False, clipboard_input=True, dialog_timeout=20, send_key_delay=50,  focus_timeout=1000) -> str:
        '''
        根据下载地址下载文件
        * @param url, 下载地址
        * @param file_folder, 保存下载文件的文件夹
        * @param file_name, 保存文件名, 为None时, 使用下载资源默认文件名, 若无默认文件名则自动为下载资源生成不重复的文件名
        * @param wait_complete, 是否等待下载完成，默认为False
        * @param wait_complete_timeout,等待下载完成超时时间，单位(秒)
        * @param simulative, 模拟输入: 通过模拟人工的方式触发输入事件; 非模拟输入(自动化接口输入): 调用元素自身实现的自动化接口输入; 默认值为`False`
        * @param clipboard_input, 是否使用剪切板输入文件路径
        * @param dialog_timeout, 点击上传按钮后，等待文件选择框的最大时间,单位（秒）
        * @param send_key_delay, 两次按键之间的时间间隔，默认为50ms
        * @param focus_timeout,  点击文件选择输入框获取焦点的等待时间，单位（毫秒）
        * @return `str`, 下载完成的文件完整路径
        '''
        valid_multi('等待下载超时时间', wait_complete_timeout, [
                    (ValidPattern.Type, int),
                    (ValidPattern.Min, -1)])
        valid_multi('获取焦点等待时间', focus_timeout, [
                    (ValidPattern.Type, int),
                    (ValidPattern.Min, -1)])
        valid_multi('等待文件选择框超时时间', dialog_timeout, [
                    (ValidPattern.Type, int),
                    (ValidPattern.Min, -1)])
        try:
            automation = self._create_automation()
            # step 1: 点击弹框前，先做一些设置
            automation.before_file_dialog_open(
                saveAs_file_folder=file_folder, saveAs_file_name=file_name)

            # step 2: 打开url
            self._invoke("DownloadUrl", {'url': url})

            # step 3: 处理弹框部分(内置不弹框，只等待框处理出现)
            download_file_name = automation.saveAs_file_dialog(file_folder,
                                                               file_name=file_name,
                                                               simulative=simulative,
                                                               clipboard_input=clipboard_input,
                                                               wait_appear_timeout=dialog_timeout,
                                                               send_key_delay=send_key_delay,
                                                               focus_timeout=focus_timeout)

            # step 4:等待加载完成
            if wait_complete:
                task_id = automation.download_task_id()
                for _ in Retry(wait_complete_timeout, interval=0.5, error_message='等待下载完成超时'):
                    if automation.is_download_complete(task_id):
                        break

            return download_file_name
        finally:
            # step 5:关闭框后处理，释放资源
            automation.after_file_dialog_closed()

    def screenshot(self, folder_path, *, file_name = None, full_size=True, width = 0, height = 0) -> NoReturn:
        '''
        对网页做截图操作
        * @param folder_path, 保存到的目标文件夹
        * @param file_name, 保存到的目标文件，若空，自动生成
        * @param full_size, 是否截取完整网页，True截取完整网页，False截取可视区域，默认为True
        * @param width, 指定截图的宽度,用于某些含有内部滚动条，整个网页截图不到的情况, 值不超过4000
        * @param height, 指定截图的高度,用于某些含有内部滚动条，整个网页截图不到的情况, 值不超过20000
        '''
        if width:
            valid_multi("截图宽度", width, [(ValidPattern.Type, int), (ValidPattern.Max, 4000)])
        if height:
            valid_multi("截图高度", height, [(ValidPattern.Type, int), (ValidPattern.Max, 20000)])

        self._invoke("Screenshot",{
            'captureArea' : 'Whole' if full_size else 'ViewPort',
            'folderPath': folder_path,
            'fileName' : file_name,
            'width' : width,
            'height' : height
        })

    def screenshot_to_clipboard(self, *, full_size=True, width = 0, height = 0) -> NoReturn:
        '''
        对网页做截图操作并保存到剪贴板中
        * @param full_size, 是否截取完整网页，True截取完整网页，False截取可视区域，默认为True
        * @param width, 指定截图的宽度,用于某些含有内部滚动条，整个网页截图不到的情况。值不超过4000
        * @param height, 指定截图的宽度,用于某些含有内部滚动条，整个网页截图不到的情况。值不超过10000
        '''
        if width:
            valid_multi("截图宽度", width, [(ValidPattern.Type, int), (ValidPattern.Max, 4000)])
        if height:
            valid_multi("截图高度", height, [(ValidPattern.Type, int), (ValidPattern.Max, 10000)])

        self._invoke("ScreenshotToClipboard",{
            'captureArea' : 'Whole' if full_size else 'ViewPort',
            'width' : width,
            'height' : height
        })

    @abstractmethod
    def _create_element(self, bid, eid) -> WebElement:
        pass

    @abstractmethod
    def _create_automation(self):
        pass

    def _invoke(self, action, args=None):
        all_args = {'browserId': self.bid}
        if args is not None:
            all_args.update(args)
        return uidriver.execute(f'{self._controller}.{action}', all_args)

    @property
    def cookies(self):
        return self._cookies
