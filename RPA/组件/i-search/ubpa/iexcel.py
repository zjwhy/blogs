# -*- coding: utf-8 -*-
import re
from ubpa import iwin
from ubpa.ilog import ILog
import xlrd, xlwt
import numpy as np
import pandas as pd
import xlwings as xw
from xlwings.utils import rgb_to_int
__logger = ILog(__file__)

'''
读取单元格的值
path   excel路径
sheet  sheet名称
cell   单元格名称
'''
def read_cell(path=None,sheet=0,cell="A1"):
    __logger.echo_msg(u"ready to execute[readCell]")
    try:
        wb = xlrd.open_workbook(path)
        if type(sheet)==str:
            sht = wb.sheet_by_name(sheet)
        elif type(sheet)==int:
            sht = wb.sheet_by_index(sheet)
        position = get_split_col_row(cell)
        pos_col = position[0]
        pos_row = position[1]
        pos_col_index = get_excel_row_index(pos_col)
        co =  sht.col_values(pos_col_index,start_rowx=int(pos_row)-1,end_rowx=int(pos_row))
        if len(co) == 0:
            co = [""]

        __logger.debug('read_cell result:[' + str(co[0]) + ']')
        return co[0]
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[readCell]")


'''
写入单元格
path   excel路径
sheet  sheet名称
cell   单元格名称
text   写入excel的值
'''
def write_cell(path=None,sheet=0,cell="A1",text=None):
    __logger.echo_msg(u"ready to execute[writeCell]")
    try:
        wb = xw.Book(path)
        sht = wb.sheets[sheet]
        sht.range(cell).options(index=False,header=False).value = text
        wb.save()
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[writeCell]")


'''
读取行
path   excel路径
sheet  sheet名称
row    行数
'''
def read_row(path=None,sheet=0,cell="A1"):
    __logger.echo_msg(u"ready to execute[read_row]")
    try:
        wb = xlrd.open_workbook(path)
        if type(sheet)==str:
            sht = wb.sheet_by_name(sheet)
        elif type(sheet)==int:
            sht = wb.sheet_by_index(sheet)
        position = get_split_col_row(cell)
        pos_col = position[0]
        pos_row = position[1]
        pos_col_index = get_excel_row_index(pos_col)
        co = sht.row_values(int(pos_row)-1, start_colx=pos_col_index)

        __logger.debug('read_row result:[' + str(co) + ']')
        return co
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[read_row]")


'''
读取列
path   excel路径
sheet  sheet名称
column  列数
header  dataFrame头
'''
def read_col(path=None,sheet=0,cell="A1"):
    __logger.echo_msg(u"ready to execute[read_col]")
    col_list = []
    try:
        wb = xlrd.open_workbook(path)
        if type(sheet)==str:
            sht = wb.sheet_by_name(sheet)
        elif type(sheet)==int:
            sht = wb.sheet_by_index(sheet)
        position = get_split_col_row(cell)
        pos_col = position[0]
        pos_row = position[1]
        pos_col_index = get_excel_row_index(pos_col)
        co = sht.col_values(pos_col_index, start_rowx=int(pos_row) - 1)

        for index in range(len(co)):
            col_list.append(co[index])

        __logger.debug('read_col result:[' + str(col_list) + ']')
        return col_list

    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[read_col]")



'''
拆分行列    输入  A12   返回   ['A','12']
'''
def get_split_col_row(string):

    string = string.upper()
    return re.findall(r'[0-9]+|[A-Z]+',string)

'''
根据excel的行号如  'AB' 则返回  26   'B' 返回1
'''
def get_excel_row_index(string):

    s=0 
    for c in string:
        c = c.upper()
        s = s*26 + ord(c) - ord('A') + 1
    return s - 1


'''
插入行
path   excel路径
sheet  sheet名称
cell   单元格的值
data   插入行的值
'''
def ins_row(path=None,sheet=0,cell="A1",data=None):
    __logger.echo_msg(u"ready to execute[ins_row]")
    try:
        wb = xw.Book(path)
        sht = wb.sheets[sheet]
        sht.range(cell).api.EntireRow.Insert()
        sht.range(cell).options(index=False,header=False).value = data
        wb.save()
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[ins_row]")

'''
插入列
path   excel路径
sheet  sheet名称
cell   单元格的值
data   插入列的值
'''
def ins_col(path=None,sheet=0,cell="A1",data=None):
    __logger.echo_msg(u"ready to execute[ins_col]")
    try:
        data_list=[]
        wb = xw.Book(path)
        sht = wb.sheets[sheet]
        sht.range(cell).api.EntireColumn.Insert()
        for i in data:
            data_list.append([i])
        sht.range(cell).options(index=False).value = data_list
        wb.save()
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[ins_col]")

'''
关闭excel应用
'''
def close_excel_apps():
    iwin.do_process_close('Excel.exe')


def get_cell_color(path, sheet=0, cell="A1"):
    '''
        get_cell_color(path, sheet=0, cell="A1") -> color
            function： Get the background color of the cell
            parameter：
                path:   str           file path
                sheet:  str or int    sheet name
                cell:   str           cell
            return:
                    the background color of the cell
                    (If you have never set a cell background color,it will return None)
            instance:
                get_cell_color('C:\\iexcel.xlsx', 'sheet1', 'A1')  ->  (255,0,0)
                get_cell_color('C:\\iexcel.xlsx', 0, 'A2')  ->  (255,255,0)

                Red          (255,0,0)
                Yellow       (255,255,0)
                Blue  	     (0,0,255)
                White	     (255,255,255)
                Black	     (0,0,0)
                Green	     (0,255,0)
                Purple	     (128,0,128)
    '''
    __logger.debug(u"ready to execute[get_cell_color]")
    try:
        wb = xw.Book(path)
        sht = wb.sheets[sheet]
        rng = sht[cell]
        color = rng.color
        if color == None:
            __logger.debug(u"This cell background color is the default background color")
        return color
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[get_cell_color]")


def set_cell_color(path, sheet=0, cell="A1", color=None):
    '''
        set_cell_color(path, sheet=0, cell="A1", color=None)
            function： Set the background color of the cell
            parameter：
              path:   str                 file path
              sheet:  str or int          sheet name
              cell:   str                 cell
              color:  str or tuple        color
	                Red       '0000FF'    (255,0,0)
                    Yellow    '00FFFF'    (255,255,0)
                    Blue  	   'FF0000'   (0,0,255)
                    White	   'FFFFFF'   (255,255,255)
                    Black	   '000000'    (0,0,0)
                    Green	   '00FF00'    (0,255,0)
                    Purple	   '800080'    (128,0,128)
            instance:
            set_cell_color('C:\\iexcel.xlsx', 0, 'A1', (0,0,255))
            set_cell_color('C:\\iexcel.xlsx', 1, 'B1', (255,255,255))
            set_cell_color('C:\\iexcel.xlsx', 'sheet1', 'C1', 'FFFFFF')
            set_cell_color('C:\\iexcel.xlsx', 'sheet2', 'D1', 'FFFFFF')
    '''
    __logger.debug(u"ready to execute[set_cell_color]")
    try:
        wb = xw.Book(path)
        sht = wb.sheets[sheet]
        rng = sht[cell]
        if isinstance(color, str):
            color = int(color, 16)
        rng.color = color
        wb.save()
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[set_cell_color]")


def set_cell_font_color(path, sheet=0, cell='A1', color='000000'):
    '''
        set_cell_font_color(path, sheet=0, cell='A1', color='000000')
            function： Set the font color of the cell
            parameter：
              path:   str               file path
              sheet:  str or int        sheet name
              cell:   str               cell
              color:  str or tuple        color
	                Red       '0000FF'    (255,0,0)
                    Yellow    '00FFFF'    (255,255,0)
                    Blue  	   'FF0000'   (0,0,255)
                    White	   'FFFFFF'   (255,255,255)
                    Black	   '000000'    (0,0,0)
                    Green	   '00FF00'    (0,255,0)
                    Purple	   '800080'    (128,0,128)
            instance:
            set_cell_font_color('C:\\iexcel.xlsx', 1, 'A1', '000000')
            set_cell_font_color('C:\\iexcel.xlsx', 'sheet2', 'B2', (0,0,0))
    '''
    __logger.debug(u"ready to execute[set_cell_font_color]")
    try:
        wb = xw.Book(path)
        sht = wb.sheets[sheet]
        if isinstance(color, tuple):  # RGB元组形式
            color = rgb_to_int(color)
        else:   # str 数字 形式
            color = int(color, 16)
        rng = sht[cell]
        rng.api.Font.Color = color
        wb.save()
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[set_cell_font_color]")


def set_range_font_color(path, sheet=0, cell_1='A1', cell_2='A1', color='000000'):
    '''
        set_range_font_color(path, sheet=0, cell_1='A1', cell_2='A1',color='000000')
            function： Set the font color of the range
            parameter：
              path:   str               file path
              sheet:  str or int        sheet name
              cell_1:   str         The cell in the upper left corner
              cell_2:   str         The cell in the lower right corner
              color:  str or tuple        color
	                Red       '0000FF'    (255,0,0)
                    Yellow    '00FFFF'    (255,255,0)
                    Blue  	   'FF0000'   (0,0,255)
                    White	   'FFFFFF'   (255,255,255)
                    Black	   '000000'    (0,0,0)
                    Green	   '00FF00'    (0,255,0)
                    Purple	   '800080'    (128,0,128)
            instance:
            set_range_font_color('C:\\iexcel.xlsx', 1, 'A1', 'A2', '000000')
            set_range_font_color('C:\\iexcel.xlsx', 'sheet2', 'A1', 'A2', (0,0,0))
    '''
    __logger.debug(u"ready to execute[set_range_font_color]")
    try:
        wb = xw.Book(path)
        sht = wb.sheets[sheet]
        if isinstance(color, tuple):  # RGB元组形式
            color = rgb_to_int(color)
        else:   # str 数字 形式
            color = int(color, 16)
        rng = sht.range(cell_1, cell_2)
        rng.api.Font.Color = color
        wb.save()
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[set_range_font_color]")


def set_range_color(path, sheet=0, cell_1="A1", cell_2="A1", color=None):
    '''
        set_range_color(path, sheet=0, cell_1="A1", cell_2="A1", color=None)
            function： Set the background color of the area cell
            parameter：
              path:   str                 file path
              sheet:  str or int          sheet name
              cell_1:   str               The cell in the upper left corner
              cell_2:   str               The cell in the lower right corner
              color:  str or tuple        color
	                Red       '0000FF'    (255,0,0)
                    Yellow    '00FFFF'    (255,255,0)
                    Blue  	   'FF0000'   (0,0,255)
                    White	   'FFFFFF'   (255,255,255)
                    Black	   '000000'    (0,0,0)
                    Green	   '00FF00'    (0,255,0)
                    Purple	   '800080'    (128,0,128)
            instance:
            set_range_color('C:\\iexcel.xlsx', 1, 'A1', 'C3','000000')
            set_range_color('C:\\iexcel.xlsx', 'sheet2', 'B1', 'D5','FFFFFF')
    '''
    __logger.debug(u"ready to execute[set_range_color]")
    try:
        wb = xw.Book(path)
        sht = wb.sheets[sheet]
        rng = sht.range(cell_1, cell_2)
        if isinstance(color, str):
            color = int(color, 16)
        rng.color = color
        wb.save()
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[set_range_color]")


def del_range(path, sheet=0, cell_1="A1", cell_2="A1"):
    '''
        del_range(path, sheet=0, cell_1="A1", cell_2="A1")
            function： Clear the format and content of cells within the specified range without affecting other cells
            parameter：
              path:   str           file path
              sheet:  str or int    sheet name
              cell_1:   str         The cell in the upper left corner
              cell_2:   str         The cell in the lower right corner
            instance:
            del_range('C:\\iexcel.xlsx', 1, 'A1', 'C3')
            del_range('C:\\iexcel.xlsx', 'sheet2', 'B1', 'D5')
    '''
    __logger.debug(u"ready to execute[del_range]")
    try:
        wb = xw.Book(path)
        sht = wb.sheets[sheet]
        rng = sht.range(cell_1, cell_2)
        rng.clear()
        wb.save()
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[del_range]")


def creat_sheet(path, sheet=None, before=None):
    '''
        creat_sheet(path, sheet=None, before=None) ->   new sheet name
            function： creat a sheet
            parameter：
              path:   str           file path
              sheet:  str           sheet name
              before: str or int    the sheet before which the new sheet is added.
            return:
                    new sheet name
            instance:
            creat_sheet('C:\\Desktop\\iexcel.xlsx')
            creat_sheet('C:\\Desktop\\iexcel.xlsx','Sheet4', before=2)
    '''
    __logger.debug(u"ready to execute[creat_sheet]")
    try:
        wb = xw.Book(path)
        if isinstance(before, int):
            before = before + 1
        Sheet = xw.sheets.add(name=sheet, before=before)
        wb.save()
        return Sheet.name
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[creat_sheet]")


def copy_sheet(path, sheet=0, new_sheet_name=None):
    '''
        copy_sheet(path, sheet=0 ,new_sheet_name=None) -> new sheet name
            function： copy a sheet
            parameter：
              path:   str                 file path
              sheet:  str or int          sheet name
              new_sheet_name: str         new sheet name
            return:
                    new sheet name
            instance:
            copy_sheet('C:\\iexcel.xlsx', sheet=0)
            copy_sheet('C:\\iexcel.xlsx', sheet='Sheet1',new_sheet_name='new_sheet')
    '''
    __logger.debug(u"ready to execute[copy_sheet]")
    try:
        wb = xw.Book(path)
        sht = wb.sheets[sheet]
        sht.api.Copy(Before=sht.api)
        wb.save()
        nsht = wb.sheets[sht.index - 2]
        if new_sheet_name != None:
            nsht.name = new_sheet_name

        return nsht.name
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[copy_sheet]")


def del_sheet(path, sheet=0):
    '''
          del_sheet(path, sheet=0)
              function： delete a sheet
              parameter：
                path:   str                 file path
                sheet:  str or int          sheet name
              instance:
              del_sheet('C:\\iexcel.xlsx', sheet='sheet1')
              del_sheet('C:\\iexcel.xlsx', sheet=1)
      '''
    __logger.debug(u"ready to execute[del_sheet]")
    try:
        wb = xw.Book(path)
        sheet = wb.sheets[sheet]
        sheet.delete()
        wb.save()
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[del_sheet]")


def get_rows_count(path, sheet=0):
    '''
            get_rows_count(path, sheet=0) ->  rows_count
                function： Get the number of form rows
                parameter：
                  path:   str                  file path
                  sheet:  str or int           sheet name
                return:
                      the number of rows
                instance:
                get_rows_count('C:\\iexcel.xlsx', sheet=0) ->  10
                get_rows_count('C:\\iexcel.xlsx', sheet='Sheet1') ->  10
        '''
    __logger.debug(u"ready to execute[get_rows_count]")
    try:
        df = pd.read_excel(path, sheet_name=sheet, header=None)
        rows_count = df.shape[0]
        return rows_count
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[get_rows_count]")


def get_cols_count(path, sheet=0):
    '''
               get_cols_count(path, sheet=0)  ->  cols_count
                   function： Get the number of form columns
                   parameter：
                     path:   str                file path
                     sheet:  str or int         sheet name
                   return:
                         the number of columns
                   instance:
                   get_cols_count('C:\\iexcel.xlsx', sheet=0 ->  10
                   get_cols_count('C:\\iexcel.xlsx', sheet='Sheet1') ->  10
           '''
    __logger.debug(u"ready to execute[get_cols_count]")
    try:
        df = pd.read_excel(path, sheet_name=sheet, header=None)
        cols_count = df.shape[1]
        return cols_count
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[get_cols_count]")


