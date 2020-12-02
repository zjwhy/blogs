'''
对话框模块
'''

import win32api
import win32con
import json
import datetime
from xbot._core import robot
from xbot.app import storage


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


def show_custom_dialog(settings, *, storage_key=None) -> dict:
    '''
    打开自定义对话框
    * @param settings, 自定义对话框配置json串, json主要包含对话框标题和自定义控件配置, json结构如下:
        {
            "dialogTitle": None
            "height": 0,
            "width": 0,
            "use_wait_timeout": False,
            "timeout": 20,
            "autoCloseButton": None,
            "canRememberContent": True,
            "settings":
            {
                "buttons":[...],
                "editors":[...]
            }
        }
        * dialogTitle: 对话框标题,可为空
        * height: 对话框显示高度,默认值是0采用自适应高度
        * width: 对话框显示宽度,默认值是0采用自适应高度
        * use_wait_timeout, 是否启用默认超时机制,默认值为 `False` 不启用
        * timeout, 启动超时自动点击时的超时时间,只有在use_wait_timeout配置为True时才起效
            * 等于 0, 不等待
            * 大于 0, 等待时间
            * 等于 -1, 一直等待
        * autoCloseButton, 等待超时是自动点击的按钮,按钮来源与配置的按钮列表,可谓空
        * canRememberContent, 运行时是否允许用户使用记住输入的内容的功能
        * buttons:按钮配置json串列表,json串格式如下
            {
                "type":"Button",
                "label":"",
                "theme":"white",
                "hotkey":None
            }
            * type: 控件类型,按钮列表中只能是`'Button'`
            * label: 按钮运行时显示的文字,可为空
            * theme: 按钮运行时显示的颜色,目前仅支持白色和红色
                * `'white'`: 白色
                * `'red'`: 红色
            * hotkey: 按钮可响应的快捷键,可为空
                * Esc: 按ESC键时响应
                * Enter: 按下回车键(Enter)时响应
                * None: 不响应快捷键,为默认值 
        * editors节点中是具体的自定义控件的json配置串, 可为一个也可为多个, 目前支持的自定义控件类型及相关json配置如下:
            * `'TextBox'`, 输入框
                {
                    "type": "TextBox",
                    "label": "输入框",
                    "VariableName": "TextBox",
                    "value": None,
                    "nullText": "请输入文本内容"
                }
            * `'Nember'`, 数字框
                {
                    "type": "Number",
                    "label": "数字输入框",
                    "VariableName": "Number",
                    "value": None,
                    "maxValue": None,
                    "minValue": None,
                    "useFloat": False
                }
            * `'Password'`, 密码框
                {
                    "type": "Password",
                    "label": "密码框",
                    "VariableName": "Password",
                    "nullText": "请输入密码",
                    "value": None
                }
            * `'TextArea'`, 文本域(多行输入框)
                {
                    "type": "TextArea",
                    "label": "文本域",
                    "VariableName": "TextArea",
                    "nullText": "请输入多行文本内容",
                    "value": None,
                    "height": 80
                }
            * `'CheckBox'`, 复选框
                {
                    "type": "CheckBox",
                    "content": "复选框",
                    "VariableName": "CheckBox",
                    "value": False
                }
            * `'Select'`, 下拉框
                {
                    "type": "Select",
                    "label": "下拉框",
                    "VariableName": "Select",
                    "value": "选项1",
                    "nullText": None,
                    "isTextEditable": False,
                    "autoCloseOnSelected": False,
                    "options": [
                        "选项1",
                        "选项2",
                        "选项3"
                    ]
                }
            * `'MultiSelect'`: 多选下拉框
                {
                    "type": "MultiSelect",
                    "label": "多选下拉框",
                    "VariableName": "MultiSelect",
                    "value": [
                        "选项1",
                        "选项2"
                    ],
                    "nullText": None,
                    "isTextEditable": False,
                    "options": [
                        "选项1",
                        "选项2",
                        "选项3"
                    ]
                }
            * `'Date'`, 日期控件
                {
                    "type": "Date",
                    "label": "日期控件",
                    "VariableName": "Date",
                    "value": "2020-11-09T15:55:23.4783724+08:00",
                    "nullText": None,
                    "dateFormat": "yyyy/MM/dd"
                }
            * `'File'`, 文件选择框
                {
                    "type": "File",
                    "label": "选择文件",
                    "VariableName": "File",
                    "kind": 0,
                    "filter": "所有文件|*.*",
                    "value": None,
                    "nullText": "请输入路径"
                }
            * `'Label'`, 文本标签
                {
                    "type": "Label",
                    "value": "文字描述",
                    "fontFamily": "Microsoft YaHei UI",
                    "fontSize": 12,
                    "label": None
                }
            * `'List'`, 列表
                {
                    "type": "List",
                    "label": "列表",
                    "VariableName": "List",
                    "value": "选项1",
                    "isTextEditable": False,
                    "height": 80,
                    "autoCloseOnSelected": False,
                    "options": [
                        "选项1",
                        "选项2",
                        "选项3"
                    ]
                }
            * `'MultiList'`, 多选列表
                {
                    "type": "MultiList",
                    "label": "多选列表",
                    "VariableName": "MultiList",
                    "value": [
                        "选项1",
                        "选项2"
                    ],
                    "isTextEditable": False,
                    "options": [
                        "选项1",
                        "选项2",
                        "选项3"
                    ],
                    "height": 85
                }
            * `'DataGrid'`, 数据表格,每个settings配置中只允许最多配置一个数据表格控件
                {
                    "type": "DataGrid",
                    "label": "数据表格",
                    "height": 300
                }
        * 自定义控件的常规配置节点有:
            * `'type'`, 自定义控件类型, 必须是上面列出的类型中的一种
            * `'label'`, 自定义控件标题, 可根据具体场景随意设置
            * `'nullText'`, 空白提示信息, 当控件没有默认值时显示的提示信息, 主要用于 `输入框`, `密码框`, `文本域` 等输入类控件, 可为空
            * `'value'`, 程序运行时控件中的默认值, 可根据具体情况设置, 可为空
        * 下拉框控件中的特殊节点有:
            * `'isTextEditable'`, 下拉框是否支持编辑, 是个 `bool` 类型值, 默认为 `False` 不可编辑
            * `'value'`, 下拉框首次打开时默认选中的选项, 可为空, 不为空时其值必须是 `'options'` 集合中的某一项的 `'value'` 的值
            * `options`, 下拉框的选项集合, 字符串数组
        * 文件选择器的特殊节点有:
            * "kind": 文件选择器的具体功能, 选项如下: 
                * `'OpenFile'`, 选择文件
                * `'SaveFile'`, 保存文件
                * `'SelectFolder'`, 保存文件夹
    * @return `dict`, 返回自定义对话框处理结果
    '''

    # load local data
    if storage_key is not None:
        settings['rememberContent'] = storage.read(
            storage_key+'REMEMBER') == 'True'
        local_data = storage.read(storage_key)
        if local_data is not None:
            local_seetings = json.loads(local_data)
            editors = settings['settings']['editors']
            for editor in editors:
                if 'value' in editor and 'VariableName' in editor and editor['VariableName'] in local_seetings:
                    editor['value'] = local_seetings[editor['VariableName']]
    else:
        settings['canRememberContent'] = False
        #storage_key等于None时认为时老版本调用，默认添加确定取消按钮
        #因为新版本storage_key不会为None
        settings['settings']['buttons'] = [{'type': 'Button',
			                                'label': '确定',
			                                'theme': 'red',
			                                'hotKey': 'Return'
		                                    }, {
			                                'type': 'Button',
			                                'label': '取消',
			                                'theme': 'white',
			                                'hotKey': 'Escape'
		                                   }]
    result = robot.execute(f'Dialog.ShowCustomDialog', {
                           'settings': json.dumps(settings, ensure_ascii=False)})

    if result['success']:
        # save local data
        if storage_key is not None:
            remember_content = result['rememberContent']
            storage.write(storage_key+'REMEMBER', str(remember_content))
            if remember_content:
                if result['data'] is not None:
                    local_data = json.dumps(result['data'], ensure_ascii=True)
                    storage.write(storage_key, local_data)
            else:
                storage.write(storage_key, None)
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

    result = robot.execute(f'Dialog.ShowMessageBox', {'settings': {'title': title, 'message': message, 'button': button,
                                                                   'timeout': timeout, 'defaultButton': default_button}})
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

    result = robot.execute(f'Dialog.ShowWorkBookDialog', {
                           'settings': {'title': title, 'message': message}})
    if result['success']:
        return result['button']
    elif not result['success']:
        raise Exception(result['error'])
    else:
        return None

def show_input_dialog(title, label, typestr, *, value = None, storage_key=None) -> dict:
    '''
    打开输入对话框
    * param title, 对话框标题
    * param label, 输入框标题
    * param type, 输入框类型
       * `'input'`, 输入框
       * `'password'`, 密码框
       * `'multiInput'`, 多行输入框
    * param value, 默认值 
    * @return `dict`, 返回输入对话框处理结果
    '''

    editorType = 'TextBox'
    if typestr == 'password':
        editorType = 'Password'
    elif typestr == 'multiInput':
        editorType = 'TextArea'
    settings = _get_settings(title)
    if typestr == 'multiInput':
        settings['settings']['editors'] = [{"type": "TextArea",
                                            "label": label,
                                            "VariableName": "value",
                                            "nullText": "请输入多行文本内容",
                                            "value": value,
                                            "height": 80
                                           }]
    else:
        editorType = 'TextBox'
        if typestr == 'password':
            editorType = 'Password'
        settings['settings']['editors'] = [{'type': editorType,
			                                'label': label,
			                                'VariableName': 'value',
			                                'value': value,
			                                'nullText': '请输入文本内容'
		                                   }]
    return show_custom_dialog(settings, storage_key = storage_key)

def show_datetime_dialog(title, label, kind, formatstr, *, begin_date = None, end_date = None,  storage_key=None) -> dict:
    '''
    打开时间设置对话框
    * param title, 对话框标题
    * param label, 提示标题
    * param kind, 时间类型
        * `'date'`, 时间
        * `'dateRange'`, 时间段
    * param formatstr, 时间格式
        * `'yyyy-MM-dd'`, 年-月-日
        * `'yyyy-MM-dd HH:mm:ss'`, 年-月-日 时:分:秒
        * `'yyyy/MM/dd'`, 年/月/日
        * `'yyyy/MM/dd HH:mm:ss'`, 年/月/日 时:分:秒
    * param begin_date, 开始时间，默认值为 `None`,如果输入的数据无法转为时间格式则取当前时间日期
    * param end_date, 结束时间，默认值为 `None`,如果输入的数据无法转为时间格式则取当前时间日期
    * @return `dict`, 返回时间对话框处理结果
    '''

    # if formatstr == 'yyyy-MM-dd':
    #     format_str = '%Y-%m-%d'
    # if formatstr == 'yyyy-MM-dd HH:mm:ss':
    #     format_str = '%Y-%m-%d %H:%M:%S'
    # if formatstr == 'yyyy/MM/dd':
    #     format_str = '%Y/%m/%d'
    # if formatstr == 'yyyy/MM/dd HH:mm:ss':
    #     format_str = '%Y/%m/%d %H:%M:%S'

    # try:
    #     datetime.datetime.strptime(begin_date, format_str)
    # except:
    #     begin_date = str(datetime.datetime.now().strftime(format_str))

    # try:
    #     datetime.datetime.strptime(end_date, format_str)
    # except:
    #     end_date = str(datetime.datetime.now().strftime(format_str))

    settings = _get_settings(title)
    if kind == 'date':
        settings['settings']['editors'] = [{"type": "Date",
                                            "label": label,
                                            "VariableName": "begin_date",
                                            "value": begin_date,
                                            "nullText": None,
                                            "dateFormat": formatstr}]
    elif kind == 'dateRange':
        settings['settings']['editors'] = [{"type": "Label",
                                            "value": label,
                                            "fontFamily": "Microsoft YaHei UI",
                                            "fontSize": 12,
                                            "label": None
                                           },
                                           {"type": "Date",
                                            "label": "开始日期",
                                            "VariableName": "begin_date",
                                            "value": begin_date,
                                            "nullText": None,
                                            "dateFormat": formatstr
                                           },
                                           {"type": "Date",
                                            "label": "结束日期",
                                            "VariableName": "end_date",
                                            "value": end_date,
                                            "nullText": None,
                                            "dateFormat": formatstr
                                           }]

    return show_custom_dialog(settings, storage_key = storage_key)

def show_select_dialog(title, label, select_type, select_model, *, values = None, is_selected_first = True, storage_key=None) -> dict:
    '''
    打开时间设置对话框
    * param title, 对话框标题
    * param label, 提示标题
    * param select_type, 选择框类型
        * `'combobox'`, 下拉框
        * `'list'`, 列表
    * param select_model, 选择模式
        * `'single'`, 单选
        * `'multi'`, 多选
    * param values, 选项列表,如 ['选项1', '选项2', '选项3']
    * param is_selected_first, 是否默认选中第一项，默认值为 `True`, 默认选中
    * @return `dict`, 返回选择对话框处理结果
    '''

    editorType = 'Select'
    if select_type == 'combobox':
        if select_model == 'single':
            editorType = 'Select'
        elif select_model == 'multi':
            editorType = 'MultiSelect'
    elif select_type == 'list':
        if select_model == 'single':
            editorType = 'List'
        elif select_model == 'multi':
            editorType = 'MultiList'

    if isinstance(values, str):
        value_array = values.split('\r\n')
    elif isinstance(values, list):
        value_array = [str(x) for x in values]
    else:
        raise ValueError("values类型不正确")

    settings = _get_settings(title)

    if editorType == 'Select' or editorType == 'MultiSelect':
        settings['settings']['editors'] = [{'type': editorType,
			                                'label': label,
			                                'VariableName': 'values',
			                                'value': None,
                                            'isTextEditable': False,
                                            'options': value_array,
                                            'nullText':None
		                                   }]
    elif editorType == 'List' or editorType == 'MultiList':
        settings['settings']['editors'] = [{'type': editorType,
			                                'label': label,
			                                'VariableName': 'values',
			                                'value': None,
                                            'options': value_array,
                                            "height": 100,
                                            'nullText':None
		                                   }]

    if is_selected_first and isinstance(value_array, list) and len(value_array) > 0:
        editors = settings['settings']['editors']
        for editor in editors:
            editor['value'] = value_array[0]

    return show_custom_dialog(settings, storage_key = storage_key)


def show_select_file_dialog(title, *, folder = None, filter = '所有文件 (.*)|*.*', is_multi = False, 
                            is_checked_exists = False) -> dict:
    '''
    打开时间设置对话框
    * param title, 对话框标题
    * param folder, 默认文件夹路径
    * param filter, 文件类型选择，默认是所有文件
    * param is_multi, 文件是否允许多选，默认是`'False'`,不允许多选
    * param is_checked_exists, 是否对结果路径进行存在性校验,默认值为`'False'`,不校验文件的存在性
    * @return `dict`, 返回文件选择对话框处理结果
    '''

    result = robot.execute(f'Dialog.ShowSelectFileDialog', {
                           'settings':{'title': title, 'folder': folder, 'filter': filter, 
                                    'is_multi': is_multi, 'is_checked_exists': is_checked_exists, }})
    if result['success']:
        return result['data']
    else:
        raise Exception(result['error'])

def show_select_folder_dialog(title, *, folder = None) -> dict:
    '''
    打开时间设置对话框
    * param title, 对话框标题
    * param folder, 默认文件夹路径
    * @return `dict`, 返回文件夹选择对话框处理结果
    '''

    result = robot.execute(f'Dialog.ShowSelectFolderDialog', {
                           'settings':{'title': title, 'folder': folder}})
    if result['success']:
        return result['data']
    else:
        raise Exception(result['error'])

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

def _get_settings(title):
    settings={'dialogTitle': title,
	          'height': 0,
	          'width': 400,
	          'timeout': 0,
	          'autoCloseButton': None,
	          'settings': {
		        'buttons': [{
			        'type': 'Button',
			        'label': '确定',
			        'theme': 'red',
			        'hotKey': 'Return'
		        }, {
			        'type': 'Button',
			        'label': '取消',
			        'theme': 'white',
			        'hotKey': 'Escape'
		        }]
	        },
	        'canRememberContent': True,
	        'rememberContent': False}
    return settings
