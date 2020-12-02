from typing import NoReturn, Any, List

from .element import MobileElement, _mobile_elements_cache
from ..selector import Selector, _get_selector_by_name
from .._core import uidriver
from .._core.validation import valid, valid_multi, ValidPattern
from ..errors import UIAError, UIAErrorCode

import time

class MobileSession(object):
    def __init__(self, controller, sid):
        self._controller = controller
        self.sid = sid
    
    def find_all(self, selector) -> List[MobileElement]:
        '''
        获取手机中与选择器匹配的全部元素并返回元素列表
        * @param selector, 要查找的选择器, 支持以下格式: 
            * 选择器名称, `str`类型
            * 选择器对象, `Selector`类型
        * @return `List[MobileElement]`, 返回手机中与目标元素相似的元素列表 
        '''

        _mobile_elements_cache.release()

        if isinstance(selector, str):
            selector = _get_selector_by_name(selector)

        if not isinstance(selector, Selector):
            raise ValueError('selector参数类型不正确')
       
        element_id_list = self._invoke('QuerySelectorAll', {'selector': selector.value})
        return [self._create_element(eid) for eid in element_id_list]
    
    def find(self, selector) -> MobileElement:
        '''
        获取手机中与元素选择器匹配的元素, 如果找到多个或者未找到相似的元素则抛出 `UIAError` 异常
         * @param selector, 要查找的选择器, 支持以下格式: 
            * 选择器名称, `str`类型
            * 选择器对象, `Selector`类型
        * @return `MobileElement`, 返回手机元素
        '''

        if isinstance(selector, str):
            selector = _get_selector_by_name(selector)

        elements = self.find_all(selector)
        if len(elements) == 0:
            raise UIAError('未找到控件', UIAErrorCode.NoSuchElement)
        elif len(elements) > 1:
            raise UIAError('匹配到多个控件, 无法唯一定位', UIAErrorCode.Common)
        else:
            return elements[0]
    
    def find_all_by_id(self, id) -> List[MobileElement]:
        '''
        获取手机中指定resource-id的全部元素并返回元素列表
        * @param id, 元素的resource-id属性值
        * @return `List[MobileElement]`, 返回元素列表
        '''

        _mobile_elements_cache.release()
        
        element_id_list = self._invoke('QueryIdSelectorAll', {'id': id})
        return [self._create_element(eid) for eid in element_id_list]
    
    def find_by_id(self, id) -> MobileElement:
        '''
        获取手机中指定resource-id的元素, 如果找到多个或者未找到相似的元素则抛出 `UIAError` 异常
         * @param id, 元素的resource-id属性值
         * @return `MobileElement`, 返回手机元素
        '''

        elements = self.find_all_by_id(id)
        if len(elements) == 0:
            raise UIAError('未找到控件', UIAErrorCode.NoSuchElement)
        elif len(elements) > 1:
            raise UIAError('匹配到多个控件, 无法唯一定位', UIAErrorCode.Common)
        else:
            return elements[0]
    
    def find_all_by_accessibility_id(self, accessibility_id) -> List[MobileElement]:
        '''
        获取手机中指定accessibility_id的全部元素并返回元素列表
        * @param accessibility_id, 元素的content-desc属性值
        * @return `List[MobileElement]`, 返回元素列表
        '''

        _mobile_elements_cache.release()

        element_id_list = self._invoke('QueryAccessibilityIdSelectorAll', {'accessibilityId': accessibility_id})
        return [self._create_element(eid) for eid in element_id_list]
    
    def find_by_accessibility_id(self, accessibility_id) -> MobileElement:
        '''
        获取手机中指定accessibility_id的元素, 如果找到多个或者未找到相似的元素则抛出 `UIAError` 异常
         * @param accessibility_id, 元素的content-desc属性值
         * @return `MobileElement`, 返回手机元素
        '''

        elements = self.find_all_by_accessibility_id(accessibility_id)
        if len(elements) == 0:
            raise UIAError('未找到控件', UIAErrorCode.NoSuchElement)
        elif len(elements) > 1:
            raise UIAError('匹配到多个控件, 无法唯一定位', UIAErrorCode.Common)
        else:
            return elements[0]

    def find_all_by_label_name(self, label_name) -> List[MobileElement]:
        '''
        获取手机中指定label_name的全部元素并返回元素列表
        * @param label_name, 元素的class属性值/元素的标签名
        * @return `List[MobileElement]`, 返回元素列表
        '''

        _mobile_elements_cache.release()

        element_id_list = self._invoke('QueryLabelNameSelectorAll', {'labelName': label_name})
        return [self._create_element(eid) for eid in element_id_list]
    
    def find_by_label_name(self, label_name) -> MobileElement:
        '''
        获取手机中指定label_name的元素, 如果找到多个或者未找到相似的元素则抛出 `UIAError` 异常
         * @param label_name, 元素的class属性值/元素的标签名
         * @return `MobileElement`, 返回手机元素
        '''

        elements = self.find_all_by_label_name(label_name)
        if len(elements) == 0:
            raise UIAError('未找到控件', UIAErrorCode.NoSuchElement)
        elif len(elements) > 1:
            raise UIAError('匹配到多个控件, 无法唯一定位', UIAErrorCode.Common)
        else:
            return elements[0]

    def find_all_by_xpath(self, xpath) -> List[MobileElement]:
        '''
        获取手机中指定xpath的全部元素并返回元素列表
        * @param xpath, 元素的xpath路径
        * @return `List[MobileElement]`, 返回元素列表
        '''

        _mobile_elements_cache.release()

        element_id_list = self._invoke('QueryXpathSelectorAll', {'xpath': xpath})
        return [self._create_element(eid) for eid in element_id_list]
    
    def find_by_xpath(self, xpath) -> MobileElement:
        '''
        获取手机中指定xpath的元素, 如果找到多个或者未找到相似的元素则抛出 `UIAError` 异常
         * @param xpath, 元素的xpath路径
         * @return `MobileElement`, 返回手机元素
        '''

        elements = self.find_all_by_xpath(xpath)
        if len(elements) == 0:
            raise UIAError('未找到控件', UIAErrorCode.NoSuchElement)
        elif len(elements) > 1:
            raise UIAError('匹配到多个控件, 无法唯一定位', UIAErrorCode.Common)
        else:
            return elements[0]
    
    def find_all_by_uiautomator_selector(self, uiautomator_selector) -> List[MobileElement]:
        '''
        获取手机中指定uiautomator_selector的全部元素并返回元素列表
        * @param uiautomator_selector, 元素的android selector
        * @return `List[MobileElement]`, 返回元素列表
        '''

        _mobile_elements_cache.release()
        
        element_id_list = self._invoke('QueryUiautomatorSelectorSelectorAll', {'uiautomatorSelector': uiautomator_selector})
        return [self._create_element(eid) for eid in element_id_list]

    def find_by_uiautomator_selector(self, uiautomator_selector) -> MobileElement:
        '''
        获取手机中指定uiautomator_selector的元素, 如果找到多个或者未找到相似的元素则抛出 `UIAError` 异常
         * @param uiautomator_selector, 元素的android selector
         * @return `MobileElement`, 返回手机元素
        '''

        elements = self.find_all_by_uiautomator_selector(uiautomator_selector)
        if len(elements) == 0:
            raise UIAError('未找到控件', UIAErrorCode.NoSuchElement)
        elif len(elements) > 1:
            raise UIAError('匹配到多个控件, 无法唯一定位', UIAErrorCode.Common)
        else:
            return elements[0]

    def close(self) -> NoReturn:
        '''
        关闭此手机连接
        '''

        self._invoke("Close")

    def swipe(self, start_point_x, start_point_y, end_point_x, end_point_y, *, swipe_time=800, delay_after=1) -> NoReturn:
        '''
        在手机屏幕上滑动手指
        * @param start_point_x, 滑动起始点横向坐标
        * @param start_point_y, 滑动起始点纵向坐标
        * @param end_point_x, 滑动结束点横向坐标
        * @param end_point_y, 滑动结束点纵向坐标
        * @param swipe_time, 滑动总时间
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        '''

        self._invoke("Swipe", {
                                'startPointX': start_point_x,
                                'startPointY': start_point_y,
                                'endPointX': end_point_x,
                                'endPointY': end_point_y,
                                'swipeTime': swipe_time
                              }
                    )
        
        if delay_after > 0:
            time.sleep(delay_after)
    
    def click(self, point_x, point_y, *, delay_after=1) -> NoReturn:
        '''
        单击手机屏幕
        * @param point_x, 目标点的横向坐标
        * @param point_y, 目标点的纵向坐标
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        '''

        self._invoke('Click', {'pointX': point_x, 'pointY': point_y})

        if delay_after > 0:
            time.sleep(delay_after)
    
    def dblclick(self, point_x, point_y, *, delay_after=1) -> NoReturn:
        '''
        双击手机屏幕
        * @param point_x, 目标点的横向坐标
        * @param point_y, 目标点的纵向坐标
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        '''

        self._invoke('DblClick', {'pointX': point_x, 'pointY': point_y})

        if delay_after > 0:
            time.sleep(delay_after)
    
    def longpress(self, point_x, point_y, *, delay_after=1) -> NoReturn:
        '''
        长按手机屏幕
        * @param point_x, 目标点的横向坐标
        * @param point_y, 目标点的纵向坐标
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        '''

        self._invoke('LongPress', {'pointX': point_x, 'pointY': point_y})
        
        if delay_after > 0:
            time.sleep(delay_after)
    
    def back(self, delay_after=1) -> NoReturn:
        '''
        后退
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        '''

        self._invoke("Back")

        if delay_after > 0:
            time.sleep(delay_after)
    
    def home(self, delay_after=1) -> NoReturn:
        '''
        主页
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        '''

        self._invoke("Home")

        if delay_after > 0:
            time.sleep(delay_after)
    
    def switchapp(self, delay_after=1) -> NoReturn:
        '''
        切换应用
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        '''

        self._invoke("SwitchApp")

        if delay_after > 0:
            time.sleep(delay_after)
    
    def enter(self, delay_after=1) -> NoReturn:
        '''
        回车确认
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        '''

        self._invoke("Enter")

        if delay_after > 0:
            time.sleep(delay_after)
    
    def getoriention(self) -> int:
        '''
        获取手机当前的屏幕方向
        * @return `int`, 横屏返回 0, 竖屏返回 1
        '''

        return self._invoke("GetOriention")
    
    def setoriention(self, screenOrientation:int) -> NoReturn:
        '''
        设置手机的屏幕方向
        * @param screenOrientation
            * 0, 横屏
            * 1, 竖屏
        '''
        self._invoke("SetOriention", {'screenOrientation': screenOrientation})

    def screenshot(self, folder_path, *, filename=None) -> NoReturn:
        '''
        对手机屏幕进行截图并保存
        * @param folder_path, 截图保存的路径
        * @param filename, 截图保存时的文件名, 可为空, 为空时会更具当前时间自动生成文件名
        '''

        valid('保存文件夹', folder_path, ValidPattern.NotEmpty)
        self._invoke('Screenshot', { 'folderPath': folder_path, 'fileName': filename })
    
    def get_page_source(self) -> str:
        '''
        获取手机当前页面的树结构信息，返回XML结构的字符串
        * @return `str`, 获取到的UI树
        '''

        return self._invoke('GetPageSource')
    
    def get_window_size(self) -> tuple:
        '''
        获取手机屏幕分辨率
        * @return `tuple`, 获取到的手机屏幕分辨率
        '''
        size = self._invoke('GetWindowSize')
        return (size['x'], size['y'])

    def set_clipboard_text(self, value) -> NoReturn:
        '''
        设置剪贴板文本内容
        * @param value，文本内容
        '''
        self._invoke("SetClipboardText", {'value': value})
    
    def get_clipboard_text(self) -> str:
        '''
        获取剪贴板文本内容
        * @return `str`, 返回文本内容
        '''
        return self._invoke("GetClipboardText")
    
    def push_file(self, file_path, path_on_device) -> NoReturn:
        '''
        将本机PC中的指定文件推送到手机中的指定位置
        * @param file_path，本地PC中的文件
        * @param path_on_device，手机中的指定位置
        '''
        self._invoke("PushFile", {'filePath': file_path, 'pathOnDevice':path_on_device})
    
    def pull_file(self, path_on_device, file_path) -> NoReturn:
        '''
        拉取手机中的指定文件，并保存到本机PC中的指定位置
        * @param path_on_device，手机中的指定文件位置
        * @param file_path，本机PC中的指定位置
        '''
        self._invoke("PullFile", {'pathOnDevice':path_on_device, 'filePath': file_path})

    def get_session_detail(self) -> dict:
        '''
        获取连接信息详情
        * @return `dict`, 返回连接信息详情
        '''
        session_detail_dict = self._invoke("GetSessionDetail")
        session_detail_dict['custom_name'] = self.custom_name   # 自定义手机名称应该属于连接详情的内容
        return session_detail_dict

    def contains_element(self, selector) -> bool:
        '''
        当前手机中是否包含与元素选择器匹配的元素
        * @param selector, 要查找的选择器, 支持以下格式: 
            * 选择器名称, `str`类型
            * 选择器对象, `Selector`类型
        * @return `bool`, 如果手机包含目标元素则返回`True`, 否则返回`False`
        '''

        if isinstance(selector, str):
            selector = _get_selector_by_name(selector)

        if not isinstance(selector, Selector):
            raise ValueError('selector参数类型不正确')

        element_count = self._invoke('GetElementCount', { 'selector': selector.value })
        if element_count == 0:
            return False
        else:
            return True
    
    def _create_element(self, eid) -> MobileElement:
        return MobileElement('MobileElement', self.sid, eid)
        
    def _invoke(self, action, args=None):
        all_args = {'sessionId': self.sid}
        if args is not None:
            all_args.update(args)
        return uidriver.execute(f'{self._controller}.{action}', all_args)
    