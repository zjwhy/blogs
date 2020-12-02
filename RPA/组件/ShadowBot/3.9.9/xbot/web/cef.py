from .automation import WebAutomation
from .browser import WebBrowser
from .element import WebElement
from .._core.retry import Retry


class CEFElement(WebElement):
    '''
    内置影刀浏览器元素模块
    '''

    def __init__(self, bid, eid):
        super().__init__('CEFElement', bid, eid)

    def _create_element(self, bid, eid):
        return CEFElement(bid, eid)

    def _create_automation(self):
        return CEFAutomation()


class CEFBrowser(WebBrowser):
    '''
    内置影刀浏览器模块
    '''

    def __init__(self, bid):
        super().__init__('CEFBrowser', bid)

    def _create_element(self, bid, eid):
        return CEFElement(bid, eid)

    def _create_automation(self):
        return CEFAutomation()


class CEFAutomation(WebAutomation):
    '''
    内置影刀浏览器自动化模块
    '''

    def __init__(self):
        super().__init__('CEF')

    def _create_browser(self, bid) -> CEFBrowser:
        return CEFBrowser(bid)

    # clipboard_input send_key_delay focus_timeout 在cef中都是没有用的, 只是为了做重载放在这里
    def choose_file_dialog(self, filenames, simulative=False, clipboard_input=True,  wait_appear_timeout=20, force_ime_ENG=False, send_key_delay=50, focus_timeout=1000):
        for _ in Retry(wait_appear_timeout, interval=0.5, error_message='等待对话框出现超时'):
            if self._invoke('IsFileDialogOpened'):
                break

    def saveAs_file_dialog(self, file_folder, *, file_name=None, simulative=False, clipboard_input=True, wait_appear_timeout=20, force_ime_ENG=False, send_key_delay=50, focus_timeout=1000) -> str:
        for _ in Retry(wait_appear_timeout, interval=0.5, error_message='等待对话框出现超时'):
            if self._invoke('IsFileDialogOpened'):
                return self._invoke('GetDownloadFilePath')
