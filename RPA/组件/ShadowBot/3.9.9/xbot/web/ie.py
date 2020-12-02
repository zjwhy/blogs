from .automation import WebAutomation
from .browser import WebBrowser
from .element import WebElement
from ..errors import UIAError, UIAErrorCode
from .._core.validation import valid, valid_multi, ValidPattern

executable_path=None


class IEElement(WebElement):
    '''
    Internet Explorer浏览器元素模块
    '''

    def __init__(self, bid, eid):
        super().__init__('IEElement', bid, eid)

    def _create_element(self, bid, eid):
        return IEElement(bid, eid)

    def _create_automation(self):
        return IEAutomation()

class IEBrowser(WebBrowser):
    '''
    Internet Explorer浏览器模块
    '''

    def __init__(self, bid):
        super().__init__('IEBrowser', bid)

    def _create_element(self, bid, eid):
        return IEElement(bid, eid)

    def _create_automation(self):
        return IEAutomation()

class IEAutomation(WebAutomation):
    '''
    Internet Explorer浏览器自动化模块
    '''

    def __init__(self):
        super().__init__('IE')

    def create(self, url, *, load_timeout=20, stop_if_timeout=False, arguments=None) -> WebBrowser:
        """
        打开网页并返回网页对象
        * @param url, 指定目标网页的地址
        * @param load_timeout, 等待网页加载的超时时间, 默认超时时间20s, 如果超出该时间网页仍未加载完成则抛出`UIAError`的异常
        * @param stop_if_timeout, 网页加载超时时是否停止加载网页, 默认是 `False` 不停止加载
        * @param arguments, 命令行参数, 必须是目标浏览器支持的命令行, 可为空
        * @return `WebBrowser`, 返回打开的网页对象
        """

        valid('网址', url, ValidPattern.NotEmpty)
        valid_multi('页面加载超时时间', load_timeout, [
                    (ValidPattern.Type, int),
                    (ValidPattern.Min, -1)])
        bid = self._invoke('CreateBrowser', {
                           'url': url, 'ieFileName': executable_path, 'arguments':arguments})
        browser = self._create_browser(bid)
        try:
            browser.wait_load_completed(load_timeout)
        except UIAError as e:
            if e.code == UIAErrorCode.Timeout and stop_if_timeout:
                browser.stop_load()
            else:
                raise e
        return browser

    def _create_browser(self, bid) -> IEBrowser:
        return IEBrowser(bid)
