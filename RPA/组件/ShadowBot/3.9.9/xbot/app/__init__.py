
'''
程序功能控制模块，如读写数据表格、展示对话框、记录日志等
'''

from .import logging, dialog, databook
import os
import json

def get_app_params(param_name) -> str:
    param_value = os.environ.get(param_name)
    return param_value