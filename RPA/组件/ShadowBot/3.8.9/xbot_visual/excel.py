from ._core import visual_action, parseint_from_args, parsefloat_from_args, excel_column_name_to_index, excel_column_index_to_name
import xbot.excel

import typing


@visual_action
def launch(**args) -> xbot.excel.workbook.baseworkbook.BaseWorkBook:
    """
    {
        'launch_way':'create',
        'open_filename': '...',
        'save_filename': '...',
        'driver_way':'openpyxl'/'office'/'wps'/'auto_check',
        'isvisible':True/False
    }
    """
    open_filename = args['open_filename']
    save_filename = args['save_filename']
    isvisible = args.get('isvisible', True)

    if args['launch_way'] == 'create':
        workbook = xbot.excel.create(kind = args['driver_way'], visible = isvisible)
        workbook.original_file = save_filename
        return workbook
    elif args['launch_way'] == 'open':
        return xbot.excel.open(open_filename, kind = args['driver_way'], visible = isvisible)


@visual_action
def get_active_workbook(**args) -> xbot.excel.workbook.baseworkbook.BaseWorkBook:
    return xbot.excel.get_active_workbook()


@visual_action
def save(**args) -> None:
    """
    {
        'excel_instance': ''
        'filename': '...'
        'save_way':'save/saveas',
        'is_close_after_save':True
    }
    """
    workbook = args['excel_instance']
    filename = args['filename']

    # 1
    if args['save_way'] == 'save':
        workbook.save()
    if args['save_way'] == 'saveas':
        workbook.save_as(filename)
    
    # 2
    if args.get('is_close_after_save', True) and not isinstance(args['excel_instance'], xbot.excel.workbook.openpyxlworkbook.OpenPyxlWorkBook):
        workbook.close()

@visual_action
def close(**args) -> None:
    """
        'excel_instance': '',
        'close_way':'notsave/save/saveas',
        'filename': '...'
    """
    workbook = args['excel_instance']
    filename = args['filename']

    if args['close_way'] == 'notsave':
        workbook.workbook.Saved = True  # self.xlApp.DisplayAlerts = False
    elif args['close_way'] == 'save':
        workbook.save()
    elif args['close_way'] == 'saveas':
        workbook.save_as(filename)
    
    if args.get('is_close_after_save', True) and not isinstance(args['excel_instance'], xbot.excel.workbook.openpyxlworkbook.OpenPyxlWorkBook):
        workbook.close()

@visual_action
def active(**args) -> None:
    """
    {
        'workbook': ''
        'mode': 'name/index'
        'value': '...'
    }
    """
    if args['mode'] == 'index':
        index = parseint_from_args(args, 'value')
        args['workbook'].active_sheet_by_index(index)
    elif args['mode'] == 'name':
        name = args['value']
        args['workbook'].active_sheet_by_name(name)


@visual_action
def create_sheet(**args):
    """
    {
        'workbook': ''
        'sheet_name': 'name'
        'create_way': 'first/last'
    }
    """
    workbook = args['workbook']
    sheet_name = args['sheet_name']
    create_way = args['create_way']

    workbook.create_sheet(sheet_name, create_way)


@visual_action
def remove_row(**args):
    """
    {
        'workbook': workbook
        'index': 1
    }
    """
    row_num = parseint_from_args(args, 'index')

    sheet = args['workbook'].get_active_sheet()
    sheet.remove_row(row_num)


@visual_action
def remove_all_rows(**args):
    """
    {
        'workbook': workbook
    }
    """
    sheet = args['workbook'].get_active_sheet()
    sheet.clear()


@visual_action
def get_row_count(**args) -> int:
    """
        'workbook': workbook
    """
    sheet = args['workbook'].get_active_sheet()
    return sheet.get_row_count()


@visual_action
def write_data_to_workbook(**args):
    """
    {
        'workbook': workbook
        'write_range': '',
        'write_way': '',
        'row_num': 1,
		'column_name': '',
        'content': '',
        'begin_row_num': 1,
		'begin_column_name': ''
    }
    """
    sheet = args['workbook'].get_active_sheet()

    row_num = parseint_from_args(args, 'row_num')
    column_name = args['column_name']
    content = args['content']

    if args['write_range'] == 'cell':
        sheet.set_cell(row_num, column_name, content)
    elif args['write_range'] == 'row':

        begin_column_name = args['begin_column_name']
        if args['write_way'] == 'append':
            sheet.append_row(content, begin_column_name = begin_column_name)
        elif args['write_way'] == 'insert':
            sheet.insert_row(row_num, content, begin_column_name = begin_column_name)
        elif args['write_way'] == 'override':
            sheet.set_row(row_num, content, begin_column_name = begin_column_name)

    elif args['write_range'] == 'column':
        begin_row_num = parseint_from_args(args, 'begin_row_num') 
        write_column_way = args.get('write_column_way', 'override')      

        begin_column_name = args['begin_column_name']
        if write_column_way == 'append':
            sheet.append_column(content, begin_row_index = begin_row_num)
        elif write_column_way == 'insert':
            sheet.insert_column(column_name, content, begin_row_index = begin_row_num)
        elif write_column_way == 'override':
            sheet.set_column(column_name, content, begin_row_num = begin_row_num)

    elif args['write_range'] == 'area':
        sheet.set_range(row_num, column_name, content)


@visual_action
def read_data_from_workbook(**args) -> typing.Any:
    """
    {
        'workbook':''
        'read_way': 'cell/range',
        'cell_row_num': '',
        'cell_column_name': ,
        'row_row_num':'',
		'area_begin_row_num': '',
		'area_begin_column_name':'',
        'area_end_row_num': '',
		'area_end_column_name':'',
        'has_header_row':'',
        'column_column_name':''
    }
    """
    sheet = args['workbook'].get_active_sheet()

    if args['read_way'] == 'cell':
        cell_row_num = parseint_from_args(args, 'cell_row_num')
        return sheet.get_cell(cell_row_num, args['cell_column_name'])
    elif args['read_way'] == 'range':

        area_begin_row_num = parseint_from_args(args, 'area_begin_row_num')
        area_begin_column_name = args['area_begin_column_name']
        area_end_row_num = parseint_from_args(args, 'area_end_row_num')
        area_end_column_name = args['area_end_column_name']
        has_header_row = args['has_header_row']

        if has_header_row == True:
            area_begin_row_num += 1
        return sheet.get_range(area_begin_row_num, area_begin_column_name, area_end_row_num, area_end_column_name)
    elif args['read_way'] == 'row':
        row_row_num = parseint_from_args(args, 'row_row_num')
        return sheet.get_row(row_row_num)
    elif args['read_way'] == 'column':
        return sheet.get_column(args['column_column_name'])

# 循环接口1.0 (before 2020.03.20)
@visual_action 
def loop_data_from_workbook(**args) -> typing.Any:
    """
    {
        'workbook':'',
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
    if isinstance(args['workbook'], xbot.excel.workbook.openpyxlworkbook.OpenPyxlWorkBook):
        return _loop_data_by_openpyxl(args)
    elif isinstance(args['workbook'], xbot.excel.workbook.comworkbook.ComWorkBook):
        return _loop_data_by_com(args)

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
    # 1、
    if isinstance(args['workbook'], xbot.excel.workbook.openpyxlworkbook.OpenPyxlWorkBook):
        data_list = _loop_data_by_openpyxl(args)
    elif isinstance(args['workbook'], xbot.excel.workbook.comworkbook.ComWorkBook):
        data_list = _loop_data_by_com(args)
    
    # 2、
    loop_way = args['loop_way']
    if loop_way == 'loop_row':
        begin_row_num = parseint_from_args(args, 'begin_row_num') - 1
        for item in data_list:
            begin_row_num+=1
            yield (item , begin_row_num , None)
    elif loop_way == 'loop_column':
        begin_column_name = args['begin_column_name']
        begin_column_index = excel_column_name_to_index(begin_column_name) - 1
        for item in data_list:
            begin_column_index+=1
            yield (item , -1, excel_column_index_to_name(begin_column_index))
    elif loop_way == 'loop_range':
        range_begin_row_num = parseint_from_args(args, 'range_begin_row_num') - 1
        for item in data_list:
            range_begin_row_num+=1
            yield (item , range_begin_row_num , None)


@visual_action
def execute_macro(**args):
    workbook = args['workbook']
    macro = args['macro']

    workbook.execute_macro(macro)


@visual_action
def select_range(**args):
    """
    {
        'workbook':,
        'select_way':'absolute_range'/'relative_to_activecell',
        'begin_row_num': 1,
		'begin_column_name': 'A',
        'end_row_num': 1,
		'end_column_name': 'A',

        // 下面四个属性对应于relative_to_activecell，目前暂不实现，将来用于扩展
        'horizontal_offset_direction': 'left'/'right',
        'horizontal_offset_number': 1,
        'vertical_offset_direction': 'up'/'down',
        'vertical_offset_number': 1
    }
    """
    # 1、计算Range
    select_way = args['select_way']
    if select_way == 'absolute_range':
        begin_row_num = parseint_from_args(args, 'begin_row_num')
        begin_column_name = args['begin_column_name']
        end_row_num = parseint_from_args(args, 'end_row_num')
        end_column_name = args['end_column_name']
        sheet = args['workbook'].get_active_sheet()
        # 2、选中Range
        sheet.select_range(begin_row_num, begin_column_name, end_row_num, end_column_name)

    elif select_way == 'row':
        row_nums = args['row_num'].split(',')
        rows = [int(row) for row in row_nums]
        sheet = args['workbook'].get_active_sheet()
        sheet.select_rows(rows)

    elif select_way == 'column':
        column_name = args['column_name'].split(',')
        columns = [column for column in column_name]
        sheet = args['workbook'].get_active_sheet()
        sheet.select_columns(columns)

    elif select_way == 'relative_to_activecell':
        # 1、GetActiveCellLocation => (X, Y)
        # 2、Calculate Range
        pass
    
    

@visual_action
def get_sheet_name(**args) -> typing.Any:
    """
    {
        'workbook':
        'sheet_scope':'active_sheet'/'all_sheet'
    }
    """
    sheets = args['workbook'].get_all_sheets()
    sheet_scope = args['sheet_scope']

    if sheet_scope == 'active_sheet':
        return args['workbook'].get_active_sheet().get_name()
    elif sheet_scope == 'all_sheet':
        return [sheet.get_name() for sheet in sheets]


@visual_action
def delete_sheet(**args):
    """
    {
        'workbook':,
        'sheet_name':,
    }
    """
    workbook = args['workbook']
    sheet_name = args['sheet_name']

    workbook.delete_sheet(sheet_name)


@visual_action
def copy_sheet(**args):
    """
    {
        'workbook':,
        'sheet_name':,
        'copy_way':'copy_in_current_workbook'/'copy_to_another_workbook',
        'dest_workbook':,
        'new_sheet_name':
    }
    """
    workbook = args['workbook']
    sheet_name = args['sheet_name']
    copy_way = args.get('copy_way', 'copy_in_current_workbook')
    dest_workbook = args.get('dest_workbook')
    new_sheet_name = args['new_sheet_name']

    if copy_way == 'copy_in_current_workbook':
        workbook.copy_sheet(sheet_name, new_sheet_name)
    elif copy_way == 'copy_to_another_workbook':
        workbook.copy_sheet_to_workbook(sheet_name, dest_workbook, new_sheet_name)


@visual_action
def get_first_free_row(**args):
    """
    {
        'workbook':
    }
    """
    workbook = args['workbook']

    return workbook.get_active_sheet().get_first_free_row()


@visual_action
def get_first_free_column(**args):
    """
    {
        'workbook':
    }
    """
    workbook = args['workbook']

    return workbook.get_active_sheet().get_first_free_column()


@visual_action
def insert_row(**args):
    """
    {
        'workbook':,
        'row_num':,
        'values':,
    }
    """
    workbook = args['workbook']
    row_num = parseint_from_args(args, 'row_num')
    values = args['values']

    return workbook.get_active_sheet().insert_row(row_num, values)


@visual_action
def insert_column(**args):
    """
    {
        'workbook':,
        'column_name':,
        'values':,
    }
    """
    workbook = args['workbook']
    column_name = args['column_name']
    values = args['values']

    return workbook.get_active_sheet().insert_column(column_name, values)


@visual_action
def remove_column(**args):
    """
    {
        'workbook':,
        'column_name':
    }
    """
    workbook = args['workbook']
    column_name = args['column_name']

    return workbook.get_active_sheet().remove_column(column_name)


@visual_action
def get_first_free_row_on_column(**args):
    """
    {
        'workbook':,
        'column_name':
    }
    """
    workbook = args['workbook']
    column_name = args['column_name']

    return workbook.get_active_sheet().get_first_free_row_on_column(column_name)


@visual_action
def get_selected_range(**args):
    """
    {
         'workbook':,
    }
    """
    workbook = args['workbook']
    begin_row_num, begin_column_name, end_row_num, end_column_name = workbook.get_selected_range()
    return begin_row_num, begin_column_name, end_row_num, end_column_name


@visual_action
def clear_range(**args):
    """
    {
        'workbook'=, 
        'clear_way'='cell'/'range'/'row'/'column', 
        'cell_row_num'=, 
        'cell_column_name'=, 
        'area_begin_row_num'=, 
        'area_begin_column_name'=, 
        'area_end_row_num'=, 
        'area_end_column_name'=, 
        'row_row_num'=, 
        'column_column_name'=
    }
    """
    workbook = args['workbook']
    clear_way = args['clear_way']
    cell_row_num = parseint_from_args(args, 'cell_row_num')
    cell_column_name = args['cell_column_name']
    area_begin_row_num = parseint_from_args(args, 'area_begin_row_num')
    area_begin_column_name = args['area_begin_column_name']
    area_end_row_num = parseint_from_args(args, 'area_end_row_num')
    area_end_column_name = args['area_end_column_name']
    row_row_num = parseint_from_args(args, 'row_row_num')
    column_column_name = args['column_column_name']

    worksheet = workbook.get_active_sheet()

    if clear_way == 'cell':
        worksheet.clear_range(cell_row_num, cell_column_name, cell_row_num, cell_column_name)
    elif clear_way == 'range':
        worksheet.clear_range(area_begin_row_num, area_begin_column_name, area_end_row_num, area_end_column_name)
    elif clear_way == 'row':
        column_count = worksheet.get_column_count()
        end_column_name = excel_column_index_to_name(column_count)
        worksheet.clear_range(
            row_row_num, 
            'A', 
            row_row_num, 
            end_column_name)
    elif clear_way == 'column':
        worksheet.clear_range(
            1, 
            column_column_name, 
            worksheet.get_row_count(), 
            column_column_name)
    else:
        raise ValueError('删除方式取值不正确')


@visual_action
def copy_range(**args):
    """
    {
        'workbook'=, 
        'copy_way'='cell'/'range'/'row'/'column', 
        'cell_row_num'=, 
        'cell_column_name'=, 
        'area_begin_row_num'=, 
        'area_begin_column_name'=, 
        'area_end_row_num'=, 
        'area_end_column_name'=, 
        'row_row_num'=, 
        'column_column_name'=
    }
    """
    workbook = args['workbook']
    copy_way = args['copy_way']
    cell_row_num = parseint_from_args(args, 'cell_row_num')
    cell_column_name = args['cell_column_name']
    area_begin_row_num = parseint_from_args(args, 'area_begin_row_num')
    area_begin_column_name = args['area_begin_column_name']
    area_end_row_num = parseint_from_args(args, 'area_end_row_num')
    area_end_column_name = args['area_end_column_name']
    row_row_num = args['row_row_num']
    column_column_name = args['column_column_name']

    worksheet = workbook.get_active_sheet()

    if copy_way == 'cell':
        worksheet.copy_range(cell_row_num, cell_column_name, cell_row_num, cell_column_name)
    elif copy_way == 'range':
        worksheet.copy_range(area_begin_row_num, area_begin_column_name, area_end_row_num, area_end_column_name)
    elif copy_way == 'row':
        row_nums = row_row_num.split(',')
        worksheet.copy_rows([int(row) for row in row_nums])
    elif copy_way == 'column':
        column_names = column_column_name.split(',')
        worksheet.copy_columns([column for column in column_names])
    else:
        raise ValueError('删除方式取值不正确')  


@visual_action
def paste_range(**args):
    """
    {
        'workbook'=, 
        'row_num'=, 
        'column_name'=
        'copy_formula'=True/False
    }
    """
    workbook = args['workbook']
    row_num = parseint_from_args(args, 'row_num')
    column_name = args['column_name']
    copy_formula = args.get('copy_formula', True)

    worksheet = workbook.get_active_sheet()
    worksheet.paste_range(row_num, column_name, copy_formula)


def _loop_data_by_com(args) -> typing.Any:
    sheet = args['workbook'].get_active_sheet()
    total_count = sheet.get_row_count()

    if total_count == 0:
        return []

    if args['loop_way'] == 'loop_row':
        begin_row_num = parseint_from_args(args, 'begin_row_num')
        end_row_num = parseint_from_args(args, 'end_row_num')
        if begin_row_num == 0 or end_row_num == 0:
            return []

        begin_row_num = abs_row_index(begin_row_num, total_count)
        end_row_num = abs_row_index(end_row_num, total_count)
        if end_row_num - begin_row_num < 0:
            return []

        used_range_column_end = sheet.worksheet.UsedRange.Column + sheet.worksheet.UsedRange.Columns.Count - 1
        value = sheet.worksheet.Range(sheet.worksheet.Cells(begin_row_num, 1), sheet.worksheet.Cells(end_row_num, used_range_column_end)).Value
        if not isinstance(value, tuple):
            value = [[value]]
        for row in value:
            yield list(row)

    elif args['loop_way'] == 'loop_column':
        begin_row_num = 1
        end_row_num = total_count
        begin_column_index = excel_column_name_to_index(args['begin_column_name'])
        end_column_index = excel_column_name_to_index(args['end_column_name'])
        if end_column_index - begin_column_index < 0:
            return []

        for index_column in range(begin_column_index, end_column_index + 1):
            column_data = []
            column_name = excel_column_index_to_name(index_column)
            value = sheet.worksheet.Range(f"{column_name}{begin_row_num}:{column_name}{end_row_num}").Value
            if not isinstance(value, tuple):
                value = [[value]]
            for row in value:
                for col in row:
                    column_data.append(col)
            yield column_data

    elif args['loop_way'] == 'loop_range':
        range_begin_row_num = parseint_from_args(args, 'range_begin_row_num')
        range_end_row_num = parseint_from_args(args, 'range_end_row_num')
        range_begin_column_name = args['range_begin_column_name']
        range_end_column_name = args['range_end_column_name']
        range_begin_column_index = excel_column_name_to_index(range_begin_column_name)
        range_end_column_index = excel_column_name_to_index(range_end_column_name)

        if range_begin_row_num == 0 or range_end_row_num == 0:
            return []
        if range_end_column_index - range_begin_column_index < 0:
            return []

        range_begin_row_num = abs_row_index(range_begin_row_num, total_count)
        range_end_row_num = abs_row_index(range_end_row_num, total_count)

        if range_end_row_num - range_begin_row_num < 0: 
            return []

        value = sheet.worksheet.Range(f"{range_begin_column_name}{range_begin_row_num}:{range_end_column_name}{range_end_row_num}").Value
        if not isinstance(value, tuple):
            value = [[value]]
        for data in value:
            yield list(data)
    

def _loop_data_by_openpyxl(args) -> typing.Any:
    sheet = args['workbook'].get_active_sheet()
    total_count = sheet.get_row_count()

    if total_count == 0:
        return []

    if args['loop_way'] == 'loop_row':
        begin_row_num = parseint_from_args(args, 'begin_row_num')
        end_row_num = parseint_from_args(args, 'end_row_num')
        if begin_row_num == 0 or end_row_num == 0:
            return []

        begin_row_num = abs_row_index(begin_row_num, total_count)
        end_row_num = abs_row_index(end_row_num, total_count)

        if end_row_num - begin_row_num < 0:
            return []

        for row in sheet.worksheet.iter_rows(min_row=begin_row_num, max_row=end_row_num, values_only=False):
            yield [col.value for col in row]

    elif args['loop_way'] == 'loop_column':
        begin_row_num = 1
        end_row_num = total_count
        begin_column_name = args['begin_column_name']
        end_column_name = args['end_column_name']
        begin_column_index = excel_column_name_to_index(begin_column_name)
        end_column_index = excel_column_name_to_index(end_column_name)
        if end_column_index - begin_column_index < 0:
            return []

        for index_column in range(begin_column_index, end_column_index + 1):
            column_data = []    
            column_name = excel_column_index_to_name(index_column)
            for row in sheet.worksheet[f'{column_name}{begin_row_num}':f'{column_name}{end_row_num}']:
                for col in row:
                    column_data.append(col.value)
            yield column_data

    elif args['loop_way'] == 'loop_range':
        range_begin_row_num = parseint_from_args(args, 'range_begin_row_num')
        range_end_row_num = parseint_from_args(args, 'range_end_row_num')
        range_begin_column_name = args['range_begin_column_name']
        range_end_column_name = args['range_end_column_name']
        range_begin_column_index = excel_column_name_to_index(range_begin_column_name)
        range_end_column_index = excel_column_name_to_index(range_end_column_name)

        if range_begin_row_num == 0 or range_end_row_num == 0:
            return []
        if range_end_column_index - range_begin_column_index < 0:
            return []
            
        range_begin_row_num = abs_row_index(range_begin_row_num, total_count)
        range_end_row_num = abs_row_index(range_end_row_num, total_count)

        if range_end_row_num - range_begin_row_num < 0: 
            return []

        for row in sheet.worksheet[f'{range_begin_column_name}{range_begin_row_num}':f'{range_end_column_name}{range_end_row_num}']:
            yield [col.value for col in row]


def abs_row_index(row_index, total_count) -> int:
    if row_index < 0:
        row_index = total_count + 1 + row_index
    else:
        row_index = (total_count if (row_index > total_count) else row_index)
    return row_index