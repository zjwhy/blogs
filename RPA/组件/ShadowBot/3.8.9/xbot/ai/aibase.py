import os, typing, abc
from PIL import Image, ImageGrab
from win32 import win32gui
import xbot.win32

class AIBase:
    def ocr_from_file(self, image_path) -> typing.List[str]:
        '''
        识别文件内容
        * @param image_path, 需要被识别的文件路径
        * @return `typing.List[str]`, 返回文件识别内容的列表
        '''
        if not os.path.isfile(image_path):
            raise IOError(f"文件{image_path}不存在")
        
        image = Image.open(image_path)
        return self._recognize_text(image)

    
    def ocr_from_window(self, hwnd, region=None) -> typing.List[str]:
        '''
        识别指定窗口内容
        * @param hwnd, 窗口句柄, 可通过窗口对象`xbot.win32.window.Win32Window`的hWnd属性获得
        * @param region, 需要识别的窗口内的子区域, 默认为None识别整个窗口, region格式为(left, top, right, bottom)的元组, 如(0, 0, 100, 100)
            * left, 左上角横坐标
            * top, 左上角纵坐标
            * right, 右下角横坐标
            * bottom, 右下角纵坐标
        * @return `typing.List[str]`, 返回窗口识别内容的列表
        '''
        if hwnd == 0:
            hwnd = win32gui.GetForegroundWindow()

        window_rect = win32gui.GetWindowRect(hwnd)
        if region is not None:
            window_width = window_rect[2] - window_rect[0]
            window_height = window_rect[3] - window_rect[1]
            left = 0
            top = 0
            right = 0
            bottom = 0
            if region[0] < window_width:
                left = window_rect[0] + region[0]
            else:
                raise ValueError("提取区域超出窗口范围")
            if region[1] < window_height:
                top = window_rect[1] + region[1]
            else:
                raise ValueError("提取区域超出窗口范围")
            if region[2] < window_width:
                right = window_rect[0] + region[2]
            else:
                raise ValueError("提取区域超出窗口范围")
            if region[3] < window_height:
                bottom = window_rect[1] + region[3]
            else:
                raise ValueError("提取区域超出窗口范围")
            window_rect = (left, top, right, bottom)
            
        image = ImageGrab.grab(bbox=window_rect)
        return self._recognize_text(image)


    def ocr_from_screen(self, region=None) -> typing.List[str]:
        '''
        识别屏幕内容
        * @param region, 需要识别的屏幕内的子区域, 默认为None识别整个屏幕, region格式为(left, top, right, bottom)的元组, 如(0, 0, 100, 100)
            * left, 左上角横坐标
            * top, 左上角纵坐标
            * right, 右下角横坐标
            * bottom, 右下角纵坐标
        * @return `typing.List[str]`, 返回屏幕识别内容的列表
        '''
        image = ImageGrab.grab(bbox=region)
        return self._recognize_text(image) 


    def ocr_from_clipboard_image(self) -> typing.List[str]:
        '''
        识别剪切板中的图片
        * @return `typing.List[str]`, 返回剪切板中图片识别内容的列表
        '''        
        image = ImageGrab.grabclipboard()
        if image == None:
            raise ValueError("剪切板中没有图片")
        return self._recognize_text(image) 


    def hover_on_text_in_screen(self, target_text, delay_after=1, anchor=None, occurrence=1) -> typing.NoReturn:
        '''
        鼠标悬浮在屏幕指定的文本上
        * @param target_text, 待查找的文本
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        * @param anchor, 锚点, 鼠标悬停元素的位置以及偏移量元组, 可为 `None`, 默认值为 `None` 为 `None` 时默认点击目标中心且无偏移量, 参数结构如下:
            * `'sudoku_part'`, 鼠标悬停的位置, 默认悬停在中心
                * `'topLeft'`, 悬停在左上角
                * `'topCenter'`, 悬停在上中部
                * `'topRight'`, 悬停在右上角
                * `'middleLeft'`, 悬停在左中部
                * `'middleCenter'`, 悬停在中心
                * `'middleRight'`, 悬停在中部
                * `'bottomLeft'`, 悬停左下角
                * `'bottomCenter'`, 悬停在下中部
                * `'bottomRight'`, 悬停在右下角
                * `'random'`, 随机在元素矩形范围内选择锚点
            * `'offset_x'`, 鼠标位置的水平偏移量
            * `'offset_y'`, 鼠标位置的垂直偏移量
        * @occurrence, 如果识别到多个结果, 可以指定位置序号，从1开始。排序规则先从左向右，再从上至下
        '''
        image = self._get_screenshot()

        text_with_location_list = self._recognize_text_with_location(image)
        target_text_rectangle = self._get_target_text_rectangle(target_text, text_with_location_list, occurrence)

        xbot.win32.mouse_move_by_anchor(target_text_rectangle, anchor=anchor, delay_after=delay_after)
    

    def hover_on_text_in_window(self, hwnd, target_text, delay_after=1, anchor=None, occurrence=1) -> typing.NoReturn:
        '''
        鼠标悬浮在窗口指定的文本上
        * @param hwnd, 指定的窗口对象
        * @param target_text, 待查找的文本
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        * @param anchor, 锚点, 鼠标悬停元素的位置以及偏移量元组, 可为 `None`, 默认值为 `None` 为 `None` 时默认点击目标中心且无偏移量, 参数结构如下:
            * `'sudoku_part'`, 鼠标悬停的位置, 默认悬停在中心
                * `'topLeft'`, 悬停在左上角
                * `'topCenter'`, 悬停在上中部
                * `'topRight'`, 悬停在右上角
                * `'middleLeft'`, 悬停在左中部
                * `'middleCenter'`, 悬停在中心
                * `'middleRight'`, 悬停在中部
                * `'bottomLeft'`, 悬停左下角
                * `'bottomCenter'`, 悬停在下中部
                * `'bottomRight'`, 悬停在右下角
                * `'random'`, 随机在元素矩形范围内选择锚点
            * `'offset_x'`, 鼠标位置的水平偏移量
            * `'offset_y'`, 鼠标位置的垂直偏移量
        * @occurrence, 如果识别到多个结果, 可以指定位置序号，从1开始。排序规则先从左向右，再从上至下
        '''
        # 1、获取窗口截图
        window_rect, window_image = self._get_window_screenshot(hwnd)

        # 2、定位文本在图像中的位置
        text_with_location_list = self._recognize_text_with_location(window_image)
        target_text_rectangle = self._get_target_text_rectangle(target_text, text_with_location_list, occurrence)
        
        # 3、鼠标hover
        xbot.win32.mouse_move_by_anchor(target_text_rectangle, anchor=anchor, relative_to='window', delay_after=delay_after)
    

    def click_text_in_screen(self, target_text, button='left', click_type='click', keys='none', delay_after=1, move_mouse=True, anchor=None, occurrence=1) -> typing.NoReturn:
        '''
        鼠标点击屏幕指定的文本
        * @param target_text, 待查找的文本
        * @param button, 要点击的鼠标按键, 默认为左键
            * `'left'`, 鼠标左键
            * `'right'`, 鼠标右键
        * @param click_type, 鼠标按键的点击方式, 如单击、双击等, 默认为单击
            * `'click'`, 鼠标单击
            * `'dbclick'`, 鼠标双击
            * `'down'`, 鼠标按键按下
            * `'up'`, 鼠标按键弹起
        * @param keys, 点击鼠标按钮时的键盘辅助按钮，可以为空，默认为空
            * `'none'`, 无键盘辅助按钮
            * `'alt'`, 使用`alt`键作为辅助按钮
            * `'ctrl'`, 使用 `ctrl`键作为辅助按钮
            * `'shift'`, 使用`shift`键作为辅助按钮
            * `'win'`, 使用win(窗口)键作为辅助按钮
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        * @param move_mouse, 是否显示鼠标移动轨迹, 默认为`True`，显示鼠标移动轨迹
        * @param anchor, 锚点, 鼠标悬停元素的位置以及偏移量元组, 可为 `None`, 默认值为 `None` 为 `None` 时默认点击目标中心且无偏移量, 参数结构如下:
            * `'sudoku_part'`, 鼠标悬停的位置, 默认悬停在中心
                * `'topLeft'`, 悬停在左上角
                * `'topCenter'`, 悬停在上中部
                * `'topRight'`, 悬停在右上角
                * `'middleLeft'`, 悬停在左中部
                * `'middleCenter'`, 悬停在中心
                * `'middleRight'`, 悬停在中部
                * `'bottomLeft'`, 悬停左下角
                * `'bottomCenter'`, 悬停在下中部
                * `'bottomRight'`, 悬停在右下角
                * `'random'`, 随机在元素矩形范围内选择锚点
            * `'offset_x'`, 鼠标位置的水平偏移量
            * `'offset_y'`, 鼠标位置的垂直偏移量
        * @occurrence, 如果识别到多个结果, 可以指定位置序号，从1开始。排序规则先从左向右，再从上至下
        '''
        image = self._get_screenshot()

        text_with_location_list = self._recognize_text_with_location(image)
        target_text_rectangle = self._get_target_text_rectangle(target_text, text_with_location_list, occurrence)

        xbot.win32.mouse_click_by_anchor(target_text_rectangle, anchor=anchor, move_mouse=move_mouse,
                                            button=button, click_type=click_type, keys=keys, delay_after=delay_after)


    def click_text_in_window(self, hwnd, target_text, button='left', click_type='click', keys='none', delay_after=1, move_mouse=True, anchor=None, occurrence=1) -> typing.NoReturn:
        '''
        鼠标点击窗口指定的文本
        * @param hwnd, 指定的窗口对象
        * @param target_text, 待查找的文本
        * @param button, 要点击的鼠标按键, 默认为左键
            * `'left'`, 鼠标左键
            * `'right'`, 鼠标右键
        * @param click_type, 鼠标按键的点击方式, 如单击、双击等, 默认为单击
            * `'click'`, 鼠标单击
            * `'dbclick'`, 鼠标双击
            * `'down'`, 鼠标按键按下
            * `'up'`, 鼠标按键弹起
        * @param keys, 点击鼠标按钮时的键盘辅助按钮，可以为空，默认为空
            * `'none'`, 无键盘辅助按钮
            * `'alt'`, 使用`alt`键作为辅助按钮
            * `'ctrl'`, 使用 `ctrl`键作为辅助按钮
            * `'shift'`, 使用`shift`键作为辅助按钮
            * `'win'`, 使用win(窗口)键作为辅助按钮
        * @param delay_after, 执行成功后延迟时间, 默认延迟1s
        * @param move_mouse, 是否显示鼠标移动轨迹, 默认为`True`，显示鼠标移动轨迹
        * @param anchor, 锚点, 鼠标悬停元素的位置以及偏移量元组, 可为 `None`, 默认值为 `None` 为 `None` 时默认点击目标中心且无偏移量, 参数结构如下:
            * `'sudoku_part'`, 鼠标悬停的位置, 默认悬停在中心
                * `'topLeft'`, 悬停在左上角
                * `'topCenter'`, 悬停在上中部
                * `'topRight'`, 悬停在右上角
                * `'middleLeft'`, 悬停在左中部
                * `'middleCenter'`, 悬停在中心
                * `'middleRight'`, 悬停在中部
                * `'bottomLeft'`, 悬停左下角
                * `'bottomCenter'`, 悬停在下中部
                * `'bottomRight'`, 悬停在右下角
                * `'random'`, 随机在元素矩形范围内选择锚点
            * `'offset_x'`, 鼠标位置的水平偏移量
            * `'offset_y'`, 鼠标位置的垂直偏移量
        * @occurrence, 如果识别到多个结果, 可以指定位置序号，从1开始。排序规则先从左向右，再从上至下
        '''
        window_rect, window_image = self._get_window_screenshot(hwnd)

        text_with_location_list = self._recognize_text_with_location(window_image)
        target_text_rectangle = self._get_target_text_rectangle(target_text, text_with_location_list, occurrence)
        target_text_rectangle_in_screen = (target_text_rectangle[0] + window_rect[0], target_text_rectangle[1] + window_rect[1], target_text_rectangle[2], target_text_rectangle[3])
        
        xbot.win32.mouse_click_by_anchor(target_text_rectangle_in_screen, anchor=anchor, move_mouse=move_mouse,
                                            button=button, click_type=click_type, keys=keys, delay_after=delay_after)


    @abc.abstractmethod
    def _recognize_text(self, image):
        pass


    @abc.abstractmethod
    def _recognize_text_with_location(self, image):
        pass


    def _get_target_text_rectangle(self, target_text, text_with_location_list, occurrence) -> typing.Tuple:
        if len(text_with_location_list) == 0:
            raise ValueError('OCR引擎未在图片中识别到任意文本')

        matched_count = 0
        for text_with_location in text_with_location_list:
            if target_text in text_with_location['text']:
                matched_count+=1
                if matched_count == occurrence:
                    location = text_with_location['location']
                    return (location['left'], location['top'], location['width'], location['height'])

        raise ValueError(f'OCR引擎未在图片中识别到目标文本 \'{target_text}\'')

    
    def _get_window_screenshot(self, hwnd):
        if hwnd == 0:
            hwnd = win32gui.GetForegroundWindow()
        window_rect = win32gui.GetWindowRect(hwnd)
        window_image = ImageGrab.grab(bbox=window_rect)
        return (window_rect, window_image)
    

    def _get_screenshot(self):
        return ImageGrab.grab()