'''
工作簿模块
'''

import abc
import typing

from ..worksheet.baseworksheet import BaseWorkSheet

class BaseWorkBook(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save(self) -> typing.NoReturn:
        '''
        将工作簿保存为excel文件
        '''
    
    @abc.abstractmethod
    def save_as(self, filename) -> typing.NoReturn:
        '''
        将工作簿另存为excel文件
        * @param filename, 另存为路径
        '''

    @abc.abstractmethod
    def close(self) -> typing.NoReturn:
        '''
        关闭工作簿
        '''

    @abc.abstractmethod
    def create_sheet(self, name, create_way) -> BaseWorkSheet:
        '''
        在工作簿中创建新的sheet页
        * @param name, sheet页名称
        * @param create_way, 添加方式
            * `'first'`, 作为第一个sheet页
            * `'last'`, 作为最后一个sheet页
        * @return `BaseWorkSheet`, sheet页对象
        '''
    
    @abc.abstractmethod
    def active_sheet_by_index(self, index) -> typing.NoReturn:
        '''
        激活工作簿中指定位置的sheet页
        * @param index, 目标sheet页在工作簿中的索引位置，从1开始计数
        '''
    
    @abc.abstractmethod
    def active_sheet_by_name(self, name) -> typing.NoReturn:
        '''
        激活工作簿中指定名称的sheet页
        * @param name, 目标sheet页的名称
        '''

    @abc.abstractmethod
    def get_sheet_by_index(self, index) -> BaseWorkSheet:
        '''
        获取工作簿中指定位置的sheet页
        * @param index, 目标sheet页在工作簿中的索引位置，从1开始计数
        * @return `BaseWorkSheet`, sheet页对象
        '''
    
    @abc.abstractmethod
    def get_sheet_by_name(self, name) -> BaseWorkSheet:
        '''
        获取工作簿中指定名称的sheet页
        * @param name, 目标sheet页的名称
        * @return `BaseWorkSheet`, sheet页对象
        '''
    
    @abc.abstractmethod
    def get_active_sheet(self) -> BaseWorkSheet:
        '''
        获取工作簿中激活的sheet页
        '''
    
    @abc.abstractmethod
    def execute_macro(self, macro) -> typing.NoReturn:
        '''
        执行宏
        * @param macro, 宏名称
        '''

    @abc.abstractmethod
    def get_all_sheets(self) -> typing.List[BaseWorkSheet]:
        '''
        获取所有sheet页
        * @return `typing.List[BaseWorkSheet]`, sheet页对象列表
        '''

    @abc.abstractmethod
    def delete_sheet(self, name) -> typing.NoReturn:
        '''
        删除指定名称的sheet页
        * @param name, 待删除的Sheet页名称
        '''

    @abc.abstractmethod
    def copy_sheet(self, name, new_name) -> BaseWorkSheet:
        '''
        拷贝sheet页
        * @param name, 源Sheet页名称
        * @param new_name, 待新建的目标Sheet页名称
        '''

    @abc.abstractmethod
    def copy_sheet_to_workbook(self, name, workbook, new_name) -> BaseWorkSheet:
        '''
        拷贝sheet页
        * @param name, 源Sheet页名称
        * @param workbook, 目标Workbook名称
        * @param new_name, 待新建的目标Sheet页名称
        '''

    @abc.abstractmethod
    def get_selected_range(self) -> typing.Tuple:
        '''
        获取选中区域
        * @return `typing.Tuple`, 四元组格式为(起始单元格行号,起始单元格列名,终止单元格行号,终止单元格列名)
        '''