'''
数据表格模块
'''


from .._core.robot import execute as _execute

import typing


def get_row(row_num) -> typing.List[str]:
    '''
    获取数据表格指定行内容
    * @param row_num, 指定行号, 行号从1开始
    * @return `List[str]`, 返回读取到的内容列表, 如['a', 'b', 'c']
    '''

    return _execute(f'Workbook.GetRow', {'rowIndex': row_num - 1})

def set_row(row_num, values, begin_column_name='A') -> typing.NoReturn:
    '''
    设置数据表格行内容
    * @param row_num, 要设置的数据表格行号, 行号从1开始
    * @param values, 要设置的值, 必须是一个列表类型，如['abc', 123, 123.456]
    * @param begin_column_name, 设置开始的单元格列名, 默认值为`'A'`
    '''

    _execute(f'Workbook.SetRow', {'rowIndex': row_num - 1, 'values': values, 'beginColumnName': begin_column_name})

def append_row(values, begin_column_name = 'A') -> typing.NoReturn:
    '''
    在数据表格最后追加一行内容
    * @param values, 要设置的值, 必须是一个列表类型，如['abc', 123, 123.456]
    * @param begin_column_name, 设置开始的单元格列名, 默认值为`'A'`
    '''

    _execute(f'Workbook.AppendRow', {'values': values, 'beginColumnName': begin_column_name})

def insert_row(row_num, values, begin_column_name = 'A') -> typing.NoReturn:
    '''
    往数据表格中插入一行内容
    * @param row_num, 插入位置的行号, 行号从1开始
    * @param values, 要设置的值, 必须是一个列表类型，如['abc', 123, 123.456]
    * @param begin_column_name, 设置开始的单元格列名, 默认值为`'A'`
    '''

    _execute(f'Workbook.InsertRow', {'rowIndex': row_num - 1, 'values': values, 'beginColumnName': begin_column_name})

def remove_row(row_num) -> typing.NoReturn:
    '''
    移除数据表的某一行内容
    * @param row_num, 要移除的行号, 行号从1开始
    '''

    _execute(f'Workbook.RemoveRow', {'rowIndex': row_num - 1})

def get_cell(row_num, col_name) -> str:
    '''
    获取数据表格指定单元格内容
    * @param row_num, 指定单元格的行号,
    * @param col_name, 指定单元格的列名,
    * @return `str`, 返回数据表格指定单元格内容
    '''

    return _execute(f'Workbook.GetCell', {'rowIndex': row_num - 1, 'colName': col_name})

def set_cell(row_num, col_name, value) -> typing.NoReturn:
    '''
    设置数据表格指定单元格内容
    * @param row_num, 指定单元格的行号, 行号从1开始
    * @param col_name, 指定单元格的列名
    * @param value, 要设置到单元格中的内容, 如 'hello world'
    '''

    _execute(f'Workbook.SetCell', { 'rowIndex': row_num - 1, 'colName': col_name, 'value': value})

def get_column(col_name) -> typing.List[str]:
    '''
    获取数据表格指定列内容
    * @param col_name, 指定列名
    * @return `List[str]`, 返回读取到的内容列表, 如['a', 'b', 'c']
    '''

    return _execute(f'Workbook.GetColumn', {'colName': col_name})

def set_column(col_name, values, begin_row_num = 1) -> typing.NoReturn:
    '''
    设置数据表格列内容
    * @param col_name, 需要设置的列名
    * @param values, 要设置的值, 只能是字符串的列表, 如['val1', 'val2']
    * @param begin_row_num, 需要设置的列的起始行号, 行号从1开始
    '''

    _execute(f'Workbook.SetColumn', { 'colName': col_name, 'values': values, 'beginRowNum': begin_row_num - 1})

def clear() -> typing.NoReturn:
    '''
    清空数据表格内容
    '''

    _execute(f'Workbook.Clear', {})

def get_row_count() -> int:
    '''
    获取数据表格的总行数
    * @return `int`, 返回数据表格的总行数
    '''

    return _execute(f'Workbook.GetRowCount', {})

def get_range(area_begin_row_num, area_begin_column_name, area_end_row_num, area_end_column_name) -> typing.List[typing.List[str]]:
    '''
    获取数据表格指定区域的内容
    * @param area_begin_row_num, 起始单元格行号, 行号从1开始
    * @param area_begin_column_name, 起始单元格列名, 列名从'A'开始
    * @param area_end_row_num, 结束单元格行号, 行号从1开始
    * @param area_end_column_name, 结束单元格列名, 列名从'A'开始
    * @return `typing.List[typing.List[str]]`, 返回读取内容组合, 如[['1', '2', '3'], ['a', 'b', 'c']]
    '''

    return _execute(f'Workbook.GetRangeCells', {'areaBeginRowNum':area_begin_row_num - 1,
                                                'areaBeginColumnName':area_begin_column_name,
                                                'areaEndRowNum':area_end_row_num - 1,
                                                'areaEndColumnName':area_end_column_name})

def set_range(row_num, col_name, values) -> typing.NoReturn:
    '''
    设置数据表格指定区域内容
    * @param row_num, 设置区域起始行号, 行号从1开始
    * @param col_name, 设置区域起始列名, 列名从'A'开始
    * @param values, 要设置的内容, 必须是一个二维数组, 如[['1', '2', '3'], ['a', 'b', 'c']]
    '''

    _execute(f'Workbook.SetRangeCells', { 'rowIndex': row_num - 1, 'colName': col_name, 'values': values})
