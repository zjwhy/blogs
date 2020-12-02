from .._core import visual_action, parseint_from_args, parsefloat_from_args,excel_column_name_to_index,excel_column_index_to_name
from xbot.app import databook

import typing

@visual_action
def foreach(**args) -> typing.Iterable:
    """
    {
        'start': 1,
        'step': 1,
        'stop': -1
    }
    """
    start = parseint_from_args(args, 'start')
    step = parseint_from_args(args, 'step')
    stop = parseint_from_args(args, 'stop')
    if stop < 0:
        # +1, 索引从1开始
        stop = databook.get_row_count() - stop + 1
    # stop+1, 不包含终点
    return range(start, stop+1, step)


@visual_action
def get_row(**args) -> typing.List[any]:
    """
    {
        'index': 1
    }
    """
    index = parseint_from_args(args, 'index')
    row = databook.get_row(index)
    return row


@visual_action
def remove_row(**args):
    """
    {
        'index': 1
    }
    """
    index = parseint_from_args(args, 'index')
    databook.remove_row(index)


@visual_action
def remove_all_rows(**args):
    """
    {
    }
    """
    databook.clear()

@visual_action
def get_row_count(**args) -> int:
    """
    """
    row_count = databook.get_row_count()
    return row_count


@visual_action
def get_cell(**args) -> typing.Any:
    """
    {
        'index': 1,
        'column': ''
    }
    """
    index = parseint_from_args(args, 'index')
    cell = databook.get_cell(index, args['column'])
    return cell


@visual_action
def active(**args):
    """
    {
        'mode': 'name/index'
        'value': '...'
    }
    """
    # databook.active(args['mode'],args['value'])
    pass


@visual_action
def create_sheet(**args):
    """
    {
        'sheet_name':''
        'create_way':'first/last'
    }
    """
    # databook.add_sheet(args['sheet_name'], args['create_way'])
    pass


@visual_action
def write_data_to_workbook(**args):
    """
    {
        'write_range': '',
        'write_way': '',
        'row_num': 1,
		'column_name': '',
        'begin_row_num': 1,
		'begin_column_name': '',
		'content': ''
    }
    """
    #1、预处理
    content = args['content']
    column_name = args['column_name']
    #2、操作数据表格
    if args['write_range'] == 'cell':
        row_num = parseint_from_args(args, 'row_num') 
        databook.set_cell(row_num, column_name, content)
    elif args['write_range'] == 'row':
        #2.1 将单个值转成[]
        if not isinstance(content, (list, tuple)):    #单个值的情况
            content = [content]
        #2.2 写入数据
        begin_column_name = args['begin_column_name']
        if args['write_way'] == 'append':
            databook.append_row(content, begin_column_name)
        elif args['write_way'] == 'insert':
            row_num = parseint_from_args(args, 'row_num')
            databook.insert_row(row_num, content, begin_column_name)
        else:
            row_num = parseint_from_args(args, 'row_num')
            databook.set_row(row_num, content, begin_column_name)
    elif args['write_range'] == 'column':
        #2.1 将单个值转成[]
        if not isinstance(content, (list, tuple)):    #单个值的情况
            content = [content]
        #2.2 写入数据
        begin_row_num = parseint_from_args(args, 'begin_row_num')
        databook.set_column(column_name, content, begin_row_num)
    else:
        #2.1 转成[[]]
        if not isinstance(content, (list, tuple)):    #单个值的情况 ()
            content = [[content]]
        else:
            if len(content) == 0:           # []的情况
                content = [[]]
            else:
                if not isinstance(content[0], (list, tuple)):   # [1,2,3,4,5]的情况 (一维)
                    content = [content]

        #2.2 写入数据
        row_num = parseint_from_args(args, 'row_num')
        databook.set_range(row_num, column_name, content)

@visual_action
def read_data_from_workbook(**args) -> typing.Any:
    """
    {
        'read_way': 'cell/range',
        'cell_row_num': '',
        'cell_column_name': ,
		'area_begin_row_num': '',
		'area_begin_column_name':'',
        'area_end_row_num': '',
		'area_end_column_name':'',
        'row_row_num':'',
        'has_header_row':'',
        'column_column_name':''
    }
    """
    read_way = args['read_way']

    if read_way == 'cell':
        cell_row_num = parseint_from_args(args, 'cell_row_num')
        return databook.get_cell(cell_row_num,args['cell_column_name'])
    elif read_way == 'range':
        area_begin_row_num = parseint_from_args(args, 'area_begin_row_num')
        area_end_row_num = parseint_from_args(args, 'area_end_row_num')

        if args['has_header_row'] == True:
            area_begin_row_num = area_begin_row_num + 1
            
        return databook.get_range(area_begin_row_num, args['area_begin_column_name'], area_end_row_num, args['area_end_column_name'])
    elif args['read_way'] == 'row':
        row_row_num = parseint_from_args(args, 'row_row_num')
        return databook.get_row(row_row_num)
    elif args['read_way'] == 'column':
        return databook.get_column(args['column_column_name'])

def abs_row_index(row_index, total_count) -> int:
        if row_index < 0:
            row_index = total_count + 1 + row_index
        else:
            row_index = (total_count if (row_index > total_count) else row_index)
        return row_index

# 循环接口1.0 (before 2020.03.20)
@visual_action 
def loop_data_from_workbook(**args) -> typing.Any:
    """
    {
        'loop_way':'loop_row/loop_column/loop_range',
        'begin_row_num':'',
        'end_row_num':'',
        'begin_column_name':'',
        'end_column_name':'',
        'range_begin_row_num':'',
        'range_begin_column_name':'',
        'range_end_row_num':'',
        'range_end_column_name':''
    }
    """
    return _loop_data(args)

# 循环接口2.0
#   扩展版本1.0的接口，支持返回item的位置：(循环行->返回当前行号, 循环列->返回当前列名, 循环区域->返回当前行号)
@visual_action
def loop_data_from_workbook_with_return_item_location(**args) -> typing.Any:
    """
    {
        'loop_way':'loop_row/loop_column/loop_range',
        'begin_row_num':'',
        'end_row_num':'',
        'begin_column_name':'',
        'end_column_name':'',
        'range_begin_row_num':'',
        'range_begin_column_name':'',
        'range_end_row_num':'',
        'range_end_column_name':''
    }
    """
    loop_way = args['loop_way']
    if loop_way == 'loop_row':
        begin_row_num = parseint_from_args(args, 'begin_row_num') - 1
        for item in _loop_data(args):
            begin_row_num+=1
            yield (item , begin_row_num , None)
    elif loop_way == 'loop_column':
        begin_column_name = args['begin_column_name']
        begin_column_index = excel_column_name_to_index(begin_column_name) - 1
        for item in _loop_data(args):
            begin_column_index+=1
            yield (item , -1, excel_column_index_to_name(begin_column_index))
    elif loop_way == 'loop_range':
        range_begin_row_num = parseint_from_args(args, 'range_begin_row_num') - 1
        for item in _loop_data(args):
            range_begin_row_num+=1
            yield (item , range_begin_row_num , None)


def _loop_data(args) -> typing.Any:
    loop_way = args['loop_way']

    begin_row_num = args['begin_row_num']
    end_row_num = args['end_row_num']

    begin_column_name = args['begin_column_name']
    end_column_name = args['end_column_name']

    range_begin_row_num = args['range_begin_row_num']
    range_begin_column_name = args['range_begin_column_name']
    range_end_row_num = args['range_end_row_num']
    range_end_column_name = args['range_end_column_name']

    total_count = databook.get_row_count()
    if total_count == 0:
        return []

    if loop_way == 'loop_row':
        begin_row_num = parseint_from_args(args, 'begin_row_num')
        end_row_num = parseint_from_args(args, 'end_row_num')
        #行号为非0整数，如果起始或结束列任一为0则返回空结果
        if begin_row_num == 0 or end_row_num == 0:
            return []

        #将行号全部转为整数，-n表示倒数第n行
        begin_row_num = abs_row_index(begin_row_num, total_count)
        end_row_num = abs_row_index(end_row_num, total_count)

        #如果起始行号大于结束行号则返回空
        if end_row_num - begin_row_num < 0:
            return []
        
        for index in range(begin_row_num, end_row_num + 1):
            yield databook.get_row(index)

    elif loop_way == 'loop_column':
        begin_row_num = 1
        end_row_num = total_count
        begin_column_index = excel_column_name_to_index(begin_column_name)
        end_column_index = excel_column_name_to_index(end_column_name)

        if end_column_index - begin_column_index < 0:
            return []

        for index_column in range(begin_column_index, end_column_index + 1):
            column_date = []
            for index in range(begin_row_num, end_row_num + 1):
                column_name = excel_column_index_to_name(index_column)
                column_date.append(databook.get_cell(index,column_name))
            yield column_date

    elif loop_way == 'loop_range':
        range_begin_row_num = parseint_from_args(args, 'range_begin_row_num')
        range_end_row_num = parseint_from_args(args, 'range_end_row_num')

        if range_begin_row_num == 0 or range_end_row_num == 0:
            return[]     

        range_begin_column_index = excel_column_name_to_index(range_begin_column_name)
        range_end_column_index = excel_column_name_to_index(range_end_column_name)

        if range_end_column_index - range_begin_column_index < 0:
            return []

        range_begin_row_num = abs_row_index(range_begin_row_num, total_count)
        range_end_row_num = abs_row_index(range_end_row_num, total_count)

        if range_end_row_num - range_end_row_num < 0:
            return []

        for item in databook.get_range(range_begin_row_num, range_begin_column_name, range_end_row_num, range_end_column_name):
            yield item
