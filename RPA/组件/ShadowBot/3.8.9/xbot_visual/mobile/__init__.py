from .._core import visual_action, parseint_from_args
import typing

from . import session, element
from xbot import mobile
from xbot.app import dialog

# import psutil
import subprocess
import re

@visual_action
def connect(**args):
    """
    {
        'connect_source': 'current'/'assign',
        'connect_kind': 'local'/'dynamic',
        'custom_name': ''
    }
    """

    connect_source = args.get('connect_source', 'assign')
    if connect_source == 'current':
        # 1、查找当前的appium server的启动端口
        port = None
        process_str = subprocess.run('tasklist /svc | findstr Appium.exe', shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout
        process_list = list(re.compile('\d+').finditer(process_str))
        if len(process_list) == 0:
            raise ValueError('请先启动Appium客户端')
        for match_item in process_list:
            # netstat -ano | findstr /e /c:" 932"
            netstat_str = subprocess.run(f'netstat -ano | findstr \" {match_item.group()}$\"', shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout
            port_service = re.compile('0.0.0.0:(\d+)').search(netstat_str)
            if port_service != None:
                port = port_service.group(1)
                break
        if port is None:
            raise ValueError('请先开启Appium服务')

        # 2、查找当前连接手机的android系统版本
        android_version = subprocess.run(r'%ANDROID_HOME%\\platform-tools\\adb.exe shell getprop ro.build.version.release', shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout
        return mobile.connect(f'http://127.0.0.1:{port}/wd/hub', 'Android', android_version, 'DeviceName')
    else:
        if args.get('connect_kind', 'local') == 'local':
            return mobile.connect_by_custom_name(args['custom_name'])
        else:
            # 1、获取本地的所有手机连接配置信息
            devices = mobile.get_local_devices()
            devices_options = [{'display': device['CustomName'], 'value': device['CustomName']} for device in devices]

            # 2、打开自定义对话框
            dict_dialog_result = dialog.show_custom_dialog(
                {
                    'dialog_title': '连接手机',
                    'settings': 
                    {
                        "editors":[{
                                    "label": "自定义手机名称",
                                    "VariableName": "selected_custom_name",
                                    "type": "Select",
                                    "value": devices_options[0]['value'] if len(devices_options) > 0 else None,
                                    "options": devices_options
                                }]
                    }
                }
            )

            # 3、连接手机
            if dict_dialog_result['pressed_button'] == '确定':
                return mobile.connect_by_custom_name(dict_dialog_result['selected_custom_name'])
            else:
                return None