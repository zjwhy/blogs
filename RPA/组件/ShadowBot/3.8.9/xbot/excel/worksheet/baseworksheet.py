'''
工作表模块
'''

import abc
import typing


class BaseWorkSheet(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_cell(self, row_num, col_name) -> any:
        '''
        获取工作表中指定单元格的内容
        * @param row_num, 指定单元格的行号, 行号从1开始
        * @param col_name, 指定单元格的列名, 列名从'A'开始
        * @return `any`, 返回工作表中指定单元格内容
        '''
    
    @abc.abstractmethod
    def get_row(self, row_num) -> typing.List[any]:
        '''
        获取工作表中指定行内容
        * @param row_num, 指定行号, 行号从1开始
        * @return `List[any]`, 返回读取到的内容列表, 如['a', 'b', 'c']
        '''
    
    @abc.abstractmethod
    def get_column(self, col_name) -> typing.List[any]:
        '''
        获取数据表格指定列内容
        * @param col_name, 指定列名，列名从'A'开始
        * @return `List[any]`, 返回读取到的内容列表, 如['a', 'b', 'c']
        '''

    @abc.abstractmethod
    def get_range(self, begin_row_num, begin_column_name, end_row_num, end_column_name) -> typing.List[typing.List[any]]:
        '''
        获取工作表中指定区域的内容
        * @param begin_row_num, 起始单元格行号, 行号从1开始
        * @param begin_column_name, 起始单元格列名, 列名从'A'开始
        * @param end_row_num, 结束单元格行号, 行号从1开始
        * @param end_column_name, 结束单元格列名, 列名从'A'开始
        * @return `typing.List[typing.List[any]]`, 返回读取内容组合, 如[['1', '2', '3'], ['a', 'b', 'c']]
        '''
    
    @abc.abstractmethod
    def set_cell(self, row_num, col_name, value) -> typing.NoReturn:
        '''
        设置工作表指定单元格内容
        * @param row_num, 指定单元格的行号, 行号从1开始
        * @param col_name, 指定单元格的列名, 列名从'A'开始
        * @param value, 要设置到单元格中的内容, 如 'hello world'
        '''
    
    @abc.abstractmethod
    def set_row(self, row_num, values, begin_column_name='A') -> typing.NoReturn:
        '''
        设置工作表行内容
        * @param row_num, 要设置的行号，行号从1开始
        * @param values, 要设置的值，必须是一个列表类型，如['a', 1, 2]
        * @param begin_column_name, 设置开始的单元格列名, 默认值为`'A'`
        '''
    
    @abc.abstractmethod
    def set_column(self, col_name, values, begin_row_num = 1) -> typing.NoReturn:
        '''
        设置工作表列内容
        * @param col_name, 需要设置的列名
        * @param values, 要设置的值, 必须是一个列表类型
        * @param begin_row_num, 需要设置的列的起始行号，行号从1开始
        '''
    
    @abc.abstractmethod
    def set_range(self, row_num, col_name, values) -> typing.NoReturn:
        '''
        设置工作表指定区域内容
        * @param row_num, 设置区域起始行号, 行号从1开始
        * @param col_name, 设置区域起始列名, 列名从'A'开始
        * @param values, 要设置的内容, 必须是一个二维数组, 如[['1', '2', '3'], ['a', 'b', 'c']]
        '''
    
    @abc.abstractmethod
    def append_row(self, values, begin_column_name = 'A') -> typing.NoReturn:
        '''
        在工作表的最后追加一行内容
        * @param values, 要设置的值, 必须是一个列表类型
        * @param begin_column_name, 设置开始的单元格列名, 默认值为`'A'`
        '''
    
    @abc.abstractmethod
    def insert_row(self, row_num, values, begin_column_name = 'A') -> typing.NoReturn:
        '''
        在工作表中插入一行内容
        * @param row_num, 插入位置的行号, 行号从1开始
        * @param values, 要设置的值，必须是一个列表类型
        * @param begin_column_name, 设置开始的单元格列名, 默认值为`'A'`
        '''
    
    @abc.abstractmethod
    def remove_row(self, row_num) -> typing.NoReturn:
        '''
        移除工作表的某一行内容
        * @param row_num, 要移除的行号, 行号从1开始
        '''
    
    @abc.abstractmethod
    def clear(self) -> typing.NoReturn:
        '''
        清空工作表内容
        '''
    
    @abc.abstractmethod
    def get_row_count(self) -> int:
        '''
        获取工作表的总行数
        * @return `int`, 返回工作表的总行数
        '''

    @abc.abstractmethod
    def get_column_count(self) -> int:
        '''
        获取工作表的总列数
        * @return `int`, 返回工作表的总列数
        '''
    
    @abc.abstractmethod
    def select_range(self, begin_row_num, begin_column_name, end_row_num, end_column_name) -> typing.NoReturn:
        '''
        选中工作表的指定内容区域
        * @param begin_row_num, 起始单元格行号, 行号从1开始
        * @param begin_column_name, 起始单元格列名, 列名从'A'开始
        * @param end_row_num, 结束单元格行号, 行号从1开始
        * @param end_column_name, 结束单元格列名, 列名从'A'开始
        '''

    @abc.abstractmethod
    def select_rows(self, rows) -> typing.NoReturn:
        '''
        选中工作表的多行
        * @param rows, 行号列表，行号从1开始
        '''

    @abc.abstractmethod
    def select_columns(self, columns) -> typing.NoReturn:
        '''
        选中工作表的多列
        * @param columns, 列名列表，列名从A开始
        '''

    @abc.abstractmethod
    def get_name(self) -> str:
        '''
        获取工作表名称
        * @return `str`, 返回工作表名称
        '''

    @abc.abstractmethod
    def append_column(self, values, begin_row_index = 1) -> typing.NoReturn:
        '''
        在工作表中追加列
        * @param values, 待插入的数据
        * @param begin_row_index, 待插入的起始单元格行号, 行号从1开始
        '''

    @abc.abstractmethod
    def insert_column(self, column_name, values, begin_row_index = 1) -> typing.NoReturn:
        '''
        在工作表中插入列
        * @param column_name, 待插入的列名，从'A'开始
        * @param values, 待插入的数据
        * @param begin_row_index, 待插入的起始单元格行号, 行号从1开始
        '''

    @abc.abstractmethod
    def get_first_free_column(self) -> str:
        '''
        获取第一个可用列
        * @return `str`, 返回工作表列名
        '''

    @abc.abstractmethod
    def get_first_free_row(self) -> int:
        '''
        获取第一个可用行
        * @return `int`, 返回工作表行号
        '''

    @abc.abstractmethod
    def remove_column(self, column_name) ->typing.NoReturn:
        '''
        删除工作表的某一列内容
        * @param column_name, 待移除的列名，从'A'开始
        '''

    @abc.abstractmethod
    def get_first_free_row_on_column(self, column_name) -> int:
        '''
        获取列上第一个可用行
        * @param column_name, 待查询的列名，从'A'开始
        '''

    @abc.abstractmethod
    def clear_range(self, begin_row_num, begin_column_name, end_row_num, end_column_name) -> typing.NoReturn:
        '''
        清空区域
        * @param begin_row_num, 起始单元格行号, 行号从1开始
        * @param begin_column_name, 起始单元格列名, 列名从'A'开始
        * @param end_row_num, 结束单元格行号, 行号从1开始
        * @param end_column_name, 结束单元格列名, 列名从'A'开始
        '''

    @abc.abstractmethod
    def copy_range(self, begin_row_num, begin_column_name, end_row_num, end_column_name) -> typing.NoReturn:
        '''
        拷贝区域数据至剪切板
        * @param begin_row_num, 起始单元格行号, 行号从1开始
        * @param begin_column_name, 起始单元格列名, 列名从'A'开始
        * @param end_row_num, 结束单元格行号, 行号从1开始
        * @param end_column_name, 结束单元格列名, 列名从'A'开始
        '''

    @abc.abstractmethod
    def copy_rows(self, rows) -> typing.NoReturn:
        '''
        拷贝工作表的多行
        * @param rows, 行号列表，行号从1开始
        '''

    @abc.abstractmethod
    def copy_columns(self, columns) -> typing.NoReturn:
        '''
        拷贝工作表的多列
        * @param columns, 列名列表，列名从A开始
        '''

    @abc.abstractmethod
    def paste_range(self, row_num, column_name, copy_formula=True) -> typing.NoReturn:
        '''
        从指定单元格处粘贴剪切板数据
        * @param row_num, 起始单元格行号, 行号从1开始
        * @param column_name, 起始单元格列名, 列名从'A'开始
        * @param copy_formula, 是否拷贝单元格公式
        '''