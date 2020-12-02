'''
对话框模块
'''

import win32api
import win32con
import json
from xbot._core import robot



def show_alert(message, title='提示'):
    '''
    打开消息对话框
    * @param message, 需要在消息对话框中展示的内容
    * @param title, 消息对话框标题, 默认为'提示'
    '''
    win32api.MessageBox(0, message, title, win32con.MB_OK |
                        win32con.MB_ICONINFORMATION)


def show_confirm(message, title='请确认') -> bool:
    '''
    打开确认对话框
    * @param message, 需要在确认对话框中展示的内容
    * @param title, 确认对话框标题, 默认为'请确认'
    * @return `bool`, 返回确认对话框处理结果, 确认返回`True`, 否则返回`False`
    '''

    result = win32api.MessageBox(
        0, message, title, win32con.MB_OKCANCEL | win32con.MB_ICONQUESTION)
    return result == 1

    
def show_custom_dialog(settings) -> dict:
    '''
    打开自定义对话框
    * @param settings, 自定义对话框配置json串, json主要包含对话框标题和自定义控件配置, json结构如下:
        {
            "dialog_title": "标题",
            "default_btn": "确定",
            "timeout": 20,
            "settings":
            {
                "editors":[...]
            }
        }
        * default_btn, 等待超时是自动点击的按钮
            * 确定
            * 取消
        * timeout, 启动超时自动点击时的超时时间
            * 等于 0, 不等待
            * 大于 0, 等待时间
            * 等于 -1, 一直等待
        * editors节点中是具体的自定义控件的json配置串, 可为一个也可为多个, 目前支持的自定义控件类型有如下:
            * `'TextBox'`, 输入框
            * `'Password'`, 密码框
            * `'TextArea'`, 文本域(多行输入框)
            * `'CheckBox'`, 复选框
            * `'Select'`, 下拉框
            * `'Date'`, 日期控件
            * `'File'`, 文件选择器
        * 自定义控件的常规配置节点有:
            * `'type'`, 自定义控件类型, 必须是上面列出的类型中的一种
            * `'label'`, 自定义控件标题, 可根据具体场景随意设置
            * `'nullText'`, 空白提示信息, 当控件没有默认值时显示的提示信息, 主要用于 `输入框`, `密码框`, `文本域` 等输入类控件, 可为空
            * `'value'`, 程序运行时控件中的默认值, 可根据具体情况设置, 可为空
        * 下拉框控件中的特殊节点有:
            * `'isTextEditable'`, 下拉框是否支持编辑, 是个 `bool` 类型值, 默认为 `False` 不可编辑
            * `'value'`, 下拉框首次打开时默认选中的选项, 可为空, 不为空时其值必须是 `'options'` 集合中的某一项的 `'value'` 的值
            * `options`, 下拉框的选项集合
                * `'display'`, 下拉框选项选中时界面显示的值
                * `'value'`, 下拉框选项选中时返回的结果值
        * 文件选择器的特殊节点有:
            * "kind": 文件选择器的具体功能, 选项如下: 
                * `'OpenFile'`, 选择文件
                * `'SaveFile'`, 保存文件
                * `'SelectFolder'`, 保存文件夹
    * @return `dict`, 返回自定义对话框处理结果
    '''

    result = robot.execute(f'Dialog.ShowCustomDialog', {'settings': json.dumps(settings, ensure_ascii=False)})
    if result['success']:
        return result['data']
    else:
        raise Exception(result['error'])


def show_message_box(title, message, button='ok', *, timeout=-1, default_button=None) -> str:
    '''
    打开消息对话框
    * @param title, 消息对话框标题
    * @param message, 消息对话框要展示的信息
    * @param dialog_result, 消息对话框中的按钮, 如:
        * `'ok'`, 确定
        * `'okcancel`, 确定/取消
        * `'yesno'`, 是/否
        * `yesnocancel`, 是/否/取消
    * @param time_out, 对话框等待点击超时时间, 超过该时间还没点击则以默认按钮进行自动点击
        * 等于 -1, 一直等待
        * 等于 0, 不等待
        * 大于 0, 等待超时
    * @param default_result, 超时时默认点击的按钮, 仅在超时时间大于0时起效, 如果默认设置了默认超时时间但但未设置默认按钮的话则以第一个按钮为默认按钮
    * @return `str`, 返回消息对话框处理结果
    '''

    if default_button is None:
        default_button = _get_default_button(button)    

    result = robot.execute(f'Dialog.ShowMessageBox', {'settings':{'title':title, 'message':message, 'button':button,
                                                      'timeout':timeout, 'defaultButton':default_button}})
    if result['success']:
        return result['button']
    elif not result['success']:
        raise Exception(result['error'])
    else:
        return None


def show_workbook_dialog(title, message) -> str:
    '''
    打开数据表格对话框
    * @param title, 数据表格对框框展示时的标题
    # @oaram message, 数据表格对话框展示时的提示信息
    * @return `str`, 返回数据表格对话框处理结果
    '''

    result = robot.execute(f'Dialog.ShowWorkBookDialog', {'settings':{'title':title, 'message':message}})
    if result['success']:
        return result['button']
    elif not result['success']:
        raise Exception(result['error'])
    else:
        return None

def show_notifycation(message, *, placement='rightbottom', level='info', timeout=3):
    '''
    打开消息通知框
    # @param message, 消息通知框的通知内容
    # @param placement, 通知消息在屏幕上的显示位置,默认在屏幕右下角显示
        * 等于 `top`, 在屏幕顶部显示
        * 等于 `bottom`, 在屏幕底部显示
        * 等于 `rightbottom`, 在屏幕右下角展示
    # @param level, 消息提示框展示时的消息等级，默认等级为信息
        * 等于 `info`, 信息
        * 等于 `warning`, 警告
        * 等于 `error`, 错误
    # @param timeout, 通知信息显示时长，默认显示3s
    '''

    robot.execute(f'Dialog.ShowNotifycation', {'settings':{'message':message, 'placement':placement,
     'level':level, 'timeout': timeout}})


def _get_default_button(button) -> str:
    default_button = 'ok'
    if button is None:
        return default_button
        
    button = button.lower()
    if button == 'ok' or button == 'okcancel':
        default_button = 'ok'
    elif button == 'yesno' or button == 'yesnocancel':
        default_button = 'yes'
    return default_button