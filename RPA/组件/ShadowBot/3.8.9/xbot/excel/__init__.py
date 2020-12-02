
'''
Excel功能控制模块，如新建Excel对象、打开Excel文件等操作
'''

from .workbook.officeworkbook import OfficeWorkBook
from .workbook.wpsworkbook import WpsWorkBook
from .workbook.openpyxlworkbook import OpenPyxlWorkBook
from .workbook.baseworkbook import BaseWorkBook
from .worksheet.baseworksheet import BaseWorkSheet


import openpyxl
import pywintypes
import win32com
import win32gui

def create(*, kind='office', visible=True) -> BaseWorkBook:
    '''
    创建并返回excel对象
    * @param kind, 创建方式
        * `'office'`, 使用 Microsoft Office 创建excel对象
        * `'wps'`, 使用 WPS 创建excel对象
        * `'openpyxl'`, 使用 Openpyxl 创建excel对象
        * `'auto_check'`, 自动检查,优先使用 `office` 创建,如果本机未安装 `office` 则尝试使用 `wps` 创建,如果也未安装wps则抛出 `ValueError` 异常
    * @param visible, 用于控制自动化操作是否用户可见，并不限制自动化的能力，仅在office和wps下有效
    * @return `BaseWorkBook`, 返回创建的excel对象
    '''

    if kind == 'openpyxl':
        workbook = openpyxl.Workbook()
        return OpenPyxlWorkBook(workbook, 'create', '')
    elif kind == 'auto_check':
        try:
            xlApp = _create_instance('office')
            kind = 'office'
        except ValueError:
            xlApp = _create_instance('wps', 'office或wps')
            kind = 'wps'
    else:
        xlApp = _create_instance(kind)

    xlApp.Visible = visible
    xlApp.DisplayAlerts = False
    workbook = xlApp.Workbooks.Add()

    if kind == 'office':
        return OfficeWorkBook(workbook, 'create', '', xlApp)
    else:
        return WpsWorkBook(workbook, 'create', '', xlApp)

def open(file_name, *, kind='office', visible=True) -> BaseWorkBook:
    '''
    打开excel文件并返回excel对象
    * @param file_name, excel文件路径
    * @param kind, 打开方式
        * `'office'`, 使用 Microsoft Office 打开excel文件
        * `'wps'`, 使用 WPS 打开excel文件
        * `'openpyxl'`, 使用 Openpyxl 打开excel文件
        * `'auto_check'`, 自动检查,优先使用 `office` 打开,如果本机未安装 `office` 则尝试使用 `wps` 打开,如果也未安装wps则抛出 `ValueError` 异常
    * @param visible, 用于控制自动化操作是否用户可见，并不限制自动化的能力，仅在office和wps下有效
    * @return `BaseWorkBook`, 返回打开的excel对象
    '''

    if kind == 'openpyxl':
        try:
            workbook = openpyxl.load_workbook(file_name)
        except openpyxl.utils.exceptions.InvalidFileException:
            raise ValueError('openpyxl目前仅支持xlsx文件格式，请使用office或wps打开该文件')
        return OpenPyxlWorkBook(workbook, 'open', file_name)
    elif kind == 'auto_check':
        try:
            xlApp = _create_instance('office')
            kind = 'office'
        except ValueError:
            xlApp = _create_instance('wps', 'office或wps')
            kind = 'wps'
    else:
        xlApp = _create_instance(kind)

    xlApp.Visible = visible
    xlApp.DisplayAlerts = False
    workbook = xlApp.Workbooks.Open(file_name, 0)
    workbook.CheckCompatibility = False

    if kind == 'office':
        return OfficeWorkBook(workbook, 'open', file_name, xlApp)
    else:
        return WpsWorkBook(workbook, 'open', file_name, xlApp)



def get_active_workbook() -> BaseWorkBook:
    '''
    获取当前激活的excel文件并返回excel对象
    * @return `BaseWorkBook`, 返回打开的excel对象
    '''

    xlApp_office = None
    active_workbook_office = None
    try:
        xlApp_office = win32com.client.Dispatch('Excel.Application')
        active_workbook_office = xlApp_office.ActiveWorkbook
    except:
        pass

    xlApp_wps = None
    active_workbook_wps = None
    try:
        xlApp_wps = win32com.client.Dispatch('ket.Application')
        active_workbook_wps = xlApp_wps.ActiveWorkbook
    except:
        pass

    if active_workbook_office is not None and active_workbook_wps is not None:
        hwnd = win32gui.GetForegroundWindow()
        text = win32gui.GetWindowText(hwnd)

        if text.endswith(' - WPS Office'):
            xlApp_wps.DisplayAlerts = False
            return WpsWorkBook(active_workbook_wps, 'get_active', '', xlApp_wps)
        elif text.endswith(' - Excel'):
            xlApp_office.DisplayAlerts = False
            return OfficeWorkBook(active_workbook_office, 'get_active', '', xlApp_office)
        else:
            raise ValueError('office 和 wps 都打开了 excel，不能确定当前激活的 excel')
    else:
        if active_workbook_office is not None:
            xlApp_office.DisplayAlerts = False
            return OfficeWorkBook(active_workbook_office, 'get_active', '', xlApp_office)
        elif active_workbook_wps is not None:
            xlApp_wps.DisplayAlerts = False
            return WpsWorkBook(active_workbook_wps, 'get_active', '', xlApp_wps)
        else:
            raise ValueError('不能获取 office 或者 wps 的当前激活 excel')
        

def _create_instance(kind, error_msg=None):

    dispatch = 'Excel.Application'
    if kind == 'wps':
        dispatch = 'ket.Application'
    if error_msg is None:
        error_msg = kind
    try:
        xlApp = win32com.client.Dispatch(dispatch)
    except pywintypes.com_error:
        raise ValueError(f'请检查你的电脑是否已安装{error_msg}')
    return xlApp
        
        