from .._core import uidriver
from .session import MobileSession
from .element import MobileElement

import os
import json


def connect_by_custom_name(custom_name) -> MobileSession:
    """
    根据自定义名称连接指定的手机
    * @param custom_name, 自定义手机名称，此名称是通过手机管理器中配置的设备别名
    * @return `MobileSession`, 设备连接对象
    """
    # 1、计算连接参数
    device_info = None
    for device in get_local_devices():
        if device['CustomName'] == custom_name:
            device_info = device
            break
    
    if device_info is None:
        raise ValueError(f"设备 {custom_name} 不存在")

    # 2、连接手机
    mobile_session = connect(device_info['AppiumUrl'], device_info['PlatformName'], device_info['PlatformVersion'], device_info['DeviceName'],
                                    additional_capabilities = device_info['AdditionalCapabilities'])
    mobile_session.custom_name = custom_name    # 如果是通过配置模板创建的手机连接对象，需要记录一下
    return mobile_session


def connect(appium_url, platform_name, platform_version, device_name, *, additional_capabilities=None) -> MobileSession:
    """
    连接指定的移动设备
    * @param appium_url, 指定的Appium服务器地址，如 `http://127.0.0.1:4723/wd/hub`
    * @param platform_name, 指定的系统名称，如 `Android` 或 `iOS`
    * @param platform_version, 指定的系统版本, 如 `8.0.1`
    * @param device_name, 指定的设备型号, 如 `Galaxy S4`
    * @param additional_capabilities, 添加其他其他配置项，请输入一个python字典对象
    * @return `MobileSession`, 设备连接对象
    """
    sid = _invoke('CreateSession', 
                        {
                          'appiumUrl': appium_url, 
                          'platformName': platform_name, 
                          'platformVersion': platform_version,
                          'deviceName': device_name,
                          'additionalCapabilities': additional_capabilities
                        }
                )
    device_session = _create_session(sid)
    device_session.custom_name = ''
    return device_session


def get_local_devices():
    filepath = os.path.join(os.environ['LOCALAPPDATA'], 'ShadowBot', 'mobile_device_connects.json')

    with open(filepath, 'r', encoding='utf8') as f:
        content_str = f.read()
        if content_str.startswith(u'\ufeff'):
            content_str = content_str.encode('utf8')[3:].decode('utf8')
    
    return json.loads(content_str)


def _create_session(sid) -> MobileSession:
    return MobileSession('MobileSession', sid)
  

def _invoke(action, args=None):
    return uidriver.execute(f'Mobile.{action}', args)