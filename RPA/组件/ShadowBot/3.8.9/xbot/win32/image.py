'''
win32图像自动化模块
'''


from .._core import uidriver
from .._core.retry import Retry
from .._core.validation import valid, valid_multi, ValidPattern
from ..errors import UIAError, UIAErrorCode
from ..selector import _get_image_selector_by_name

import typing
import re
import os
import time

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

_NS_X = "{rpa://imageelement/core}"

# hWnd==0，则使用当前激活窗口，否则尝试激活指定窗口


def wait_appear(image_selectors, *, wait_all=False, timeout=20) -> bool:
    '''
    在整个屏幕中等待与图像选择器匹配的图片出现
    * @param image_selectors, 图像选择器, 支持以下格式: 
        * `'img'`或`package.image_selector('img')`, 获取名称为img的图像选择器
        * `['img1', 'img2']`或`[package.image_selector('img1'), package.image_selector('img2')]`, 获取名称为img1和img2的图像选择器组
    * @param wait_all, 是否等待全部目标图片出现后在执行, 默认值为`False`不等待全部图片出现
    * @param timeout, 等待目标图片出现的超时时间, 默认时间为20s
    * @return `bool`, 在指定延迟时间内如果目标元素出现则返回`True`, 否则返回`False`
    '''

    valid('图像选择器', image_selectors, ValidPattern.NotEmptyArray)

    image_selectors = _resolve_selector_list(image_selectors)
    for _ in Retry(timeout, interval=0.5, ignore_exception=True):
        try:
            find_result = _invoke(
                'ExistImages',
                {
                    'imageSelectors': image_selectors,
                    'findAll': wait_all
                }
            )
            if find_result == True:
                return True

        except UIAError:
            break

    return False


def wait_appear_from_window(hWnd, image_selectors, *, wait_all=False, timeout=20) -> bool:
    '''
    在指定的窗口中等待与图像选择器匹配的图片出现
    * @param hWnd, 目标窗口的句柄, 可通过窗口对象`xbot.win32.window.Win32Window`的hWnd属性获得
    * @param image_selectors, 图像选择器, 支持以下格式: 
        * `'img'`或`package.image_selector('img')`, 获取名称为img的图像选择器
        * `['img1', 'img2']`或`[package.image_selector('img1'), package.image_selector('img2')]`, 获取名称为img1和img2的图像选择器组
    * @param wait_all, 是否等待全部目标图片出现后在执行, 默认值为`False`不等待全部图片出现
    * @param timeout, 等待目标图片出现的超时时间, 默认时间为20s
    * @return `bool`, 在指定延迟时间内如果目标元素出现则返回`True`, 否则返回`False`
    '''

    valid_multi('目标窗口句柄', hWnd, [(ValidPattern.Type, int), (ValidPattern.Range, (0, 0xffffffff))])
    valid('图像选择器', image_selectors, ValidPattern.NotEmptyArray)

    image_selectors = _resolve_selector_list(image_selectors)
    for _ in Retry(timeout, interval=0.5, ignore_exception=True):
        try:
            find_result = _invoke(
                'ExistImageInWindow',
                {
                    'hWnd': hWnd,
                    'imageSelectors': image_selectors,
                    'findAll': wait_all
                }
            )
            if find_result == True:
                return True
        except UIAError:
            break

    return False


def wait_disappear(image_selectors, *, wait_all=False, timeout=20) -> bool:
    '''
    在整个屏幕中等待与图像选择器匹配的图片消失
    * @param image_selectors, 图像选择器, 支持以下格式: 
        * `'img'`或`package.image_selector('img')`, 获取名称为img的图像选择器
        * `['img1', 'img2']`或`[package.image_selector('img1'), package.image_selector('img2')]`, 获取名称为img1和img2的图像选择器组
    * @param wait_all, 是否等待全部目标图片消失后在执行, 默认值为`False`不等待全部图片消失
    * @param timeout, 等待目标图片消失的超时时间, 默认时间为20s
    * @return `bool`, 在指定延迟时间内如果目标元素出现则返回`True`, 否则返回`False`
    '''

    valid('图像选择器', image_selectors, ValidPattern.NotEmptyArray)

    image_selectors = _resolve_selector_list(image_selectors)
    for _ in Retry(timeout, interval=0.5, ignore_exception=True):
        try:
            find_result = _invoke(
                'NotExistImages',
                {
                    'imageSelectors': image_selectors,
                    'findAll': wait_all
                }
            )
            if find_result == True:
                return True

        except UIAError:
            break

    return False


def wait_disappear_from_window(hWnd, image_selectors, *, wait_all=False, timeout=20) -> bool:
    '''
    在指定的窗口中等待与图像选择器匹配的图片消失
    * @param hWnd, 目标窗口的句柄, 可通过窗口对象`xbot.win32.window.Win32Window`的hWnd属性获得
    * @param image_selectors, 图像选择器, 支持以下格式: 
        * `'img'`或`package.image_selector('img')`, 获取名称为img的图像选择器
        * `['img1', 'img2']`或`[package.image_selector('img1'), package.image_selector('img2')]`, 获取名称为img1和img2的图像选择器组
    * @param wait_all, 是否等待全部目标图片消失后在执行, 默认值为`False`不等待全部图片消失
    * @param timeout, 等待目标图片消失的超时时间, 默认时间为20s
    * @return `bool`, 在指定延迟时间内如果目标元素出现则返回`True`, 否则返回`False`
    '''

    valid_multi('目标窗口句柄', hWnd, [(ValidPattern.Type, int), (ValidPattern.Range, (0, 0xffffffff))])
    valid('图像选择器', image_selectors, ValidPattern.NotEmptyArray)

    image_selectors = _resolve_selector_list(image_selectors)
    for _ in Retry(timeout, interval=0.5, ignore_exception=True):
        try:
            find_result = _invoke(
                'NotExistImagesInWindow',
                {
                    'hWnd': hWnd,
                    'imageSelectors': image_selectors,
                    'findAll': wait_all
                }
            )
            if find_result == True:
                return True

        except UIAError:
            break

    return False


def hover(image_selectors, *, anchor=None, timeout=5, delay_after=1) -> typing.NoReturn:
    '''
    在整个屏幕上查找与图像选择器匹配的图片并将鼠标悬停在上面
    * @param image_selectors, 图像选择器, 支持以下格式: 
        * `'img'`或`package.image_selector('img')`, 获取名称为img的图像选择器
        * `['img1', 'img2']`或`[package.image_selector('img1'), package.image_selector('img2')]`, 获取名称为img1和img2的图像选择器组
    * @param anchor, 锚点, 鼠标点击元素的位置以及偏移量元组, 示例: anchor=('topLeft', 100, 100), 可为 `None`, 默认值为 `None` 为 `None` 时默认点击目标中心且无偏移量, 参数结构如下:
        * `'sudoku_part'`, 鼠标悬停的位置, 默认悬停在中心
            * `'topLeft'`, 悬停左上角
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
    * @param timeout, 获取图像元素的超时时间, 默认值为5s
    * @param delay_after, 执行成功后延迟时间, 默认延迟1s
    '''

    # 1、计算入参
    valid('图像选择器', image_selectors, ValidPattern.NotEmptyArray)

    sudoku_part, offset_x, offset_y = (
        'middleCenter', 0, 0) if anchor is None else anchor
    image_selectors = _resolve_selector_list(image_selectors)

    # 2、图像操作，支持重试
    operation_flag = False
    for _ in Retry(timeout, interval=0.5, ignore_exception=True):   # 忽略 "操作超时" 的异常
        try:
            _invoke(
                'Hover',
                {
                    'imageSelectors': image_selectors,
                    'sudokuPart': sudoku_part,
                    'offsetX': offset_x,
                    'offsetY': offset_y
                }
            )
            operation_flag = True
            break                                   # 停止重试
        except UIAError as e:
            if e.code == UIAErrorCode.NoSuchImage:  # 如果是 图像未找到 的原因，就开始下一次重试
                continue            
            else:
                raise e                             # 如果是其他原因就直接报错
            
    
    # 3、能走到这里，说明肯定是图像不存在
    if operation_flag == False:
        raise UIAError('未找到任意一幅目标图像', UIAErrorCode.NoSuchImage)

    if delay_after > 0:
        time.sleep(delay_after)


def hover_on_window(hWnd, image_selectors, *, anchor=None, timeout=5, delay_after=1) -> typing.NoReturn:
    '''
    在指定的窗口中查找与图片选择器匹配的图像并将鼠标悬停在上面
    * @param hWnd, 目标窗口的句柄, 可通过窗口对象`xbot.win32.window.Win32Window`的hWnd属性获得
    * @param image_selectors, 图像选择器, 支持以下格式: 
        * `'img'`或`package.image_selector('img')`, 获取名称为img的图像选择器
        * `['img1', 'img2']`或`[package.image_selector('img1'), package.image_selector('img2')]`, 获取名称为img1和img2的图像选择器组
    * @param anchor, 锚点, 鼠标点击元素的位置以及偏移量元组, 示例: anchor=('topLeft', 100, 100), 可为 `None`, 默认值为 `None` 为 `None` 时默认点击目标中心且无偏移量, 参数结构如下:
        * `'sudoku_part'`, 鼠标悬停的位置, 默认悬停在中心
            * `'topLeft'`, 悬停左上角
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
    * @param timeout, 获取图像元素的超时时间, 默认值为5s
    * @param delay_after, 执行成功后延迟时间, 默认延迟1s
    '''

    # 1、计算入参
    valid_multi('目标窗口句柄', hWnd, [(ValidPattern.Type, int), (ValidPattern.Range, (0, 0xffffffff))])
    valid('图像选择器', image_selectors, ValidPattern.NotEmptyArray)

    sudoku_part, offset_x, offset_y = (
        'middleCenter', 0, 0) if anchor is None else anchor
    image_selectors = _resolve_selector_list(image_selectors)

    # 2、图像操作，支持重试
    operation_flag = False
    for _ in Retry(timeout, interval=0.5, ignore_exception=True):   # 忽略 "操作超时" 的异常
        try:
            _invoke(
                'HoverOnWindow',
                {
                    'hWnd': hWnd,
                    'imageSelectors': image_selectors,
                    'sudokuPart': sudoku_part,
                    'offsetX': offset_x,
                    'offsetY': offset_y
                }
            )
            operation_flag = True
            break                                   # 停止重试
        except UIAError as e:
            if e.code == UIAErrorCode.NoSuchImage:  # 如果是 图像未找到 的原因，就开始下一次重试
                continue            
            else:
                raise e                             # 如果是其他原因就直接报错
            
    
    # 3、能走到这里，说明肯定是图像不存在
    if operation_flag == False:
        raise UIAError('未找到任意一幅目标图像', UIAErrorCode.NoSuchImage)

    if delay_after > 0:
        time.sleep(delay_after)


def click(image_selectors, *, anchor=None, button='left', keys='none', move_mouse=True, timeout=5, delay_after=1) -> typing.NoReturn:
    '''
    在这个屏幕上查找与图像选择器相似的图像并单击
    * @param image_selectors, 图像选择器, 支持以下格式: 
        * `'img'`或`package.image_selector('img')`, 获取名称为img的图像选择器
        * `['img1', 'img2']`或`[package.image_selector('img1'), package.image_selector('img2')]`, 获取名称为img1和img2的图像选择器组
    * @param anchor, 锚点, 鼠标点击元素的位置以及偏移量元组, 示例: anchor=('topLeft', 100, 100), 可为 `None`, 默认值为 `None` 为 `None` 时默认点击目标中心且无偏移量, 参数结构如下:
        * `'sudoku_part'`, 鼠标悬停的位置, 默认悬停在中心
            * `'topLeft'`, 悬停左上角
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
    * @param button, 鼠标点击时按下的按键, 默认为鼠标左键
        * `'left'`, 鼠标左键
        * `'right'`, 鼠标右键
    * @param keys， 鼠标点击时使用键盘辅助按键, 可为空, 默认为空
        * `'none'`, 不使用键盘辅助按键
        * `'alt'`, 使用键盘Alt键作为辅助按键
        * `'ctrl'`, 使用键盘Ctrl键作为辅助按键
        * `'shift'`, 使用键盘Shift键作为辅助按键
        * `'win'`, 使用Win(窗口)键作为辅助按键
    * @param move_mouse, 是否显示鼠标移动轨迹, 默认值为`True`显示鼠标移动轨迹
    * @param timeout, 获取图像元素的超时时间, 默认值为5s
    * @param delay_after, 执行成功后延迟时间, 默认延迟1s
    '''
    
    # 1、计算入参
    valid('图像选择器', image_selectors, ValidPattern.NotEmptyArray)

    sudoku_part, offset_x, offset_y = (
        'middleCenter', 0, 0) if anchor is None else anchor
    image_selectors = _resolve_selector_list(image_selectors)

    # 2、图像操作，支持重试
    operation_flag = False
    for _ in Retry(timeout, interval=0.5, ignore_exception=True):   # 忽略 "操作超时" 的异常
        try:
            _invoke(
                'Click',
                {
                    'imageSelectors': image_selectors,
                    'sudokuPart': sudoku_part,
                    'offsetX': offset_x,
                    'offsetY': offset_y,

                    'button': button,
                    'keys': keys,
                    'moveMouse': move_mouse
                }
            )
            operation_flag = True
            break                                   # 停止重试
        except UIAError as e:
            if e.code == UIAErrorCode.NoSuchImage:  # 如果是 图像未找到 的原因，就开始下一次重试
                continue            
            else:
                raise e                             # 如果是其他原因就直接报错
    
    # 3、能走到这里，说明肯定是图像不存在
    if operation_flag == False:
        raise UIAError('未找到任意一幅目标图像', UIAErrorCode.NoSuchImage)

    if delay_after > 0:
        time.sleep(delay_after)


def click_on_window(hWnd, image_selectors, *, anchor=None, button='left', keys='none', move_mouse=True, timeout=5, delay_after=1) -> typing.NoReturn:
    '''
    在指定的窗口上查找与图像选择器匹配的图像并单击
    * @param hWnd, 目标窗口的句柄, 可通过窗口对象`xbot.win32.window.Win32Window`的hWnd属性获得
    * @param image_selectors, 图像选择器, 支持以下格式: 
        * `'img'`或`package.image_selector('img')`, 获取名称为img的图像选择器
        * `['img1', 'img2']`或`[package.image_selector('img1'), package.image_selector('img2')]`, 获取名称为img1和img2的图像选择器组
    * @param anchor, 锚点, 鼠标点击元素的位置以及偏移量元组, 示例: anchor=('topLeft', 100, 100), 可为 `None`, 默认值为 `None` 为 `None` 时默认点击目标中心且无偏移量, 参数结构如下:
        * `'sudoku_part'`, 鼠标悬停的位置, 默认悬停在中心
            * `'topLeft'`, 悬停左上角
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
    * @param button, 鼠标点击时按下的按键, 默认为鼠标左键
        * `'left'`, 鼠标左键
        * `'right'`, 鼠标右键
    * @param keys， 鼠标点击时使用键盘辅助按键, 可为空, 默认为空
        * `'none'`, 不使用键盘辅助按键
        * `'alt'`, 使用键盘Alt键作为辅助按键
        * `'ctrl'`, 使用键盘Ctrl键作为辅助按键
        * `'shift'`, 使用键盘Shift键作为辅助按键
        * `'win'`, 使用Win(窗口)键作为辅助按键
    * @param move_mouse, 是否显示鼠标移动轨迹, 默认值为`True`显示鼠标移动轨迹
    * @param timeout, 获取图像元素的超时时间, 默认值为5s
    * @param delay_after, 执行成功后延迟时间, 默认延迟1s
    '''

    # 1、计算入参
    valid_multi('目标窗口句柄', hWnd, [(ValidPattern.Type, int), (ValidPattern.Range, (0, 0xffffffff))])
    valid('图像选择器', image_selectors, ValidPattern.NotEmptyArray)

    sudoku_part, offset_x, offset_y = (
        'middleCenter', 0, 0) if anchor is None else anchor
    image_selectors = _resolve_selector_list(image_selectors)

    # 2、图像操作，支持重试
    operation_flag = False
    for _ in Retry(timeout, interval=0.5, ignore_exception=True):   # 忽略 "操作超时" 的异常
        try:
            _invoke(
                'ClickOnWindow',
                {
                    'hWnd': hWnd,
                    'imageSelectors': image_selectors,
                    'sudokuPart': sudoku_part,
                    'offsetX': offset_x,
                    'offsetY': offset_y,
                    'button': button,
                    'keys': keys,
                    'moveMouse': move_mouse
                }
            )

            operation_flag = True
            break                                   # 停止重试
        except UIAError as e:
            if e.code == UIAErrorCode.NoSuchImage:  # 如果是 图像未找到 的原因，就开始下一次重试
                continue            
            else:
                raise e                             # 如果是其他原因就直接报错
    
    # 3、能走到这里，说明肯定是图像不存在
    if operation_flag == False:
        raise UIAError('未找到任意一幅目标图像', UIAErrorCode.NoSuchImage)

    if delay_after > 0:
        time.sleep(delay_after)


def dblclick(image_selectors, *, anchor=None, move_mouse=True, timeout=5, delay_after=1) -> typing.NoReturn:
    '''
    在这个屏幕上查找与图像选择器匹配的图像并双击
    * @param image_selectors, 图像选择器, 支持以下格式: 
        * `'img'`或`package.image_selector('img')`, 获取名称为img的图像选择器
        * `['img1', 'img2']`或`[package.image_selector('img1'), package.image_selector('img2')]`, 获取名称为img1和img2的图像选择器组
    * @param anchor, 锚点, 鼠标点击元素的位置以及偏移量元组, 示例: anchor=('topLeft', 100, 100), 可为 `None`, 默认值为 `None` 为 `None` 时默认点击目标中心且无偏移量, 参数结构如下:
        * `'sudoku_part'`, 鼠标悬停的位置, 默认悬停在中心
            * `'topLeft'`, 悬停左上角
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
    * @param move_mouse, 是否显示鼠标移动轨迹, 默认值为`True`显示鼠标移动轨迹
    * @param timeout, 获取图像元素的超时时间, 默认值为5s
    * @param delay_after, 执行成功后延迟时间, 默认延迟1s
    '''
    
    # 1、计算入参
    valid('图像选择器', image_selectors, ValidPattern.NotEmptyArray)

    sudoku_part, offset_x, offset_y = (
        'middleCenter', 0, 0) if anchor is None else anchor
    image_selectors = _resolve_selector_list(image_selectors)

    # 2、图像操作，支持重试
    operation_flag = False
    for _ in Retry(timeout, interval=0.5, ignore_exception=True):   # 忽略 "操作超时" 的异常
        try:
            _invoke(
                'DblClick',
                {
                    'imageSelectors': image_selectors,
                    'sudokuPart': sudoku_part,
                    'offsetX': offset_x,
                    'offsetY': offset_y,
                    'moveMouse': move_mouse
                }
            )
            operation_flag = True
            break                                   # 停止重试
        except UIAError as e:
            if e.code == UIAErrorCode.NoSuchImage:  # 如果是 图像未找到 的原因，就开始下一次重试
                continue            
            else:
                raise e                             # 如果是其他原因就直接报错
    
    # 3、能走到这里，说明肯定是图像不存在
    if operation_flag == False:
        raise UIAError('未找到任意一幅目标图像', UIAErrorCode.NoSuchImage)

    if delay_after > 0:
        time.sleep(delay_after)


def dblclick_on_window(hWnd, image_selectors, *, anchor=None, move_mouse=True, timeout=5, delay_after=1) -> typing.NoReturn:
    '''
    在指定的窗口上查找与图像选择器匹配的图像并双击
    * @param hWnd, 目标窗口的句柄, 可通过窗口对象`xbot.win32.window.Win32Window`的hWnd属性获得
    * @param image_selectors, 图像选择器, 支持以下格式: 
        * `'img'`或`package.image_selector('img')`, 获取名称为img的图像选择器
        * `['img1', 'img2']`或`[package.image_selector('img1'), package.image_selector('img2')]`, 获取名称为img1和img2的图像选择器组
    * @param anchor, 锚点, 鼠标点击元素的位置以及偏移量元组, 示例: anchor=('topLeft', 100, 100), 可为 `None`, 默认值为 `None` 为 `None` 时默认点击目标中心且无偏移量, 参数结构如下:
        * `'sudoku_part'`, 鼠标悬停的位置, 默认悬停在中心
            * `'topLeft'`, 悬停左上角
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
    * @param move_mouse, 是否显示鼠标移动轨迹, 默认值为`True`显示鼠标移动轨迹
    * @param timeout, 获取图像元素的超时时间, 默认值为5s
    * @param delay_after, 执行成功后延迟时间, 默认延迟1s
    '''

    # 1、计算入参
    valid_multi('目标窗口句柄', hWnd, [(ValidPattern.Type, int), (ValidPattern.Range, (0, 0xffffffff))])
    valid('图像选择器', image_selectors, ValidPattern.NotEmptyArray)

    sudoku_part, offset_x, offset_y = (
        'middleCenter', 0, 0) if anchor is None else anchor
    image_selectors = _resolve_selector_list(image_selectors)

    # 2、图像操作，支持重试
    operation_flag = False
    for _ in Retry(timeout, interval=0.5, ignore_exception=True):   # 忽略 "操作超时" 的异常
        try:
            _invoke(
                'DblClickOnWindow',
                {
                    'hWnd': hWnd,
                    'imageSelectors': image_selectors,
                    'sudokuPart': sudoku_part,
                    'offsetX': offset_x,
                    'offsetY': offset_y,
                    'moveMouse': move_mouse
                }
            )
            operation_flag = True
            break                                   # 停止重试
        except UIAError as e:
            if e.code == UIAErrorCode.NoSuchImage:  # 如果是 图像未找到 的原因，就开始下一次重试
                continue            
            else:
                raise e                             # 如果是其他原因就直接报错
            
    
    # 3、能走到这里，说明肯定是图像不存在
    if operation_flag == False:
        raise UIAError('未找到任意一幅目标图像', UIAErrorCode.NoSuchImage)

    if delay_after > 0:
        time.sleep(delay_after)


def _invoke(action, args=None):
    all_args = {}
    if args is not None:
        args['imageSelectors'] = [
            image_selector.value for image_selector in args['imageSelectors']]
        all_args.update(args)
    return uidriver.execute(f'Image.{action}', all_args)


def _resolve_selector_list(image_selectors):
    if image_selectors is None:
        image_selectors = []
    if not isinstance(image_selectors, (tuple, list)):
        image_selectors = [image_selectors]
    # str to ImageSelector
    for i in range(len(image_selectors)):
        if isinstance(image_selectors[i], str):
            image_selectors[i] = _get_image_selector_by_name(
                image_selectors[i])
    return image_selectors
