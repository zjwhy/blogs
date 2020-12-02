''' 

@author: ibm
'''
# -*- coding:utf-8 -*-
from ctypes import cdll
import sys, win32com.client
import time
from ubpa import iwin
from ubpa.iconstant import WAIT_FOR, TRY_INTERVAL
from ubpa.ilog import ILog
import uiautomation
from autoit import control
import ubpa.encrypt as encrypt
import ubpa.iimg as img

__logger = ILog(__file__)

class SapControl(): 
    def __init__(self, conn=0, sess=0, win=0):
        self.SapGuiAuto = win32com.client.GetObject("SAPGUI") 
        self.application = self.SapGuiAuto.GetScriptingEngine 
        self.connection = self.application.Children(conn)
        self.session = self.connection.Children(sess)
        self.win = self.session.Children(win)
        
    def getText(self,id):
        return self.win.findById(id).text
    
    def setText(self,id,text):
        self.win.findById(id).text = text
        
    def doClick(self,id): 
        self.win.findById(id).press()
    
    def findElement(self,id): 
        return self.win.findById(id) 
    

def do_click(win_title=None,id=None,row=None,col=None,button='left',curson='center',offsetX=0,offsetY=0,times=1,waitfor=WAIT_FOR,run_mode='unctrl'):
    """
    sap 鼠标点击
    """
    try:
        __logger.debug('sap do click :'+str(id))
        if run_mode == 'ctrl':
            element = get_element(id, waitfor)
            if row!=None and col!=None and element.type=='GuiShell':
                 element.setCurrentCell(row, col)
            if element.type == 'GuiButton':
                element.press()
            elif element.type == 'GuiRadioButton':
                element.select() 
            elif element.type == 'GuiCheckBox':
                element.selected = not element.selected
            else:
               element.setFocus()
        else:                
            if (win_title != None): 
                if not iwin.do_win_is_active(win_title):
                    iwin.do_win_activate(win_title=win_title, waitfor=waitfor)
            x,y = __get_element_pos(id, row ,col,curson, offsetX, offsetY, waitfor) 
            
            for i in range(times):
                if button == 'left':
                    uiautomation.Win32API.MouseClick(x,y,0)
                elif button == 'right':
                    uiautomation.Win32API.MouseRightClick(x,y,0)
                else:
                    uiautomation.Win32API.MouseMiddleClick(x,y,0)
                time.sleep(uiautomation.Win32API.GetDoubleClickTime() * 1.0 / 2000)
    except Exception as e:
        raise e



def do_moveto_pos(win_title=None,id=None,row=None,col=None,curson='center',offsetX=0,offsetY=0,waitfor=WAIT_FOR):
    '''
    鼠标移动到指定位置
    ''' 
    try:
        __logger.debug('sap do moveto :'+str(id))
        if (win_title != None): 
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)
        x,y = __get_element_pos(id, row,col,curson, offsetX, offsetY, waitfor)
        uiautomation.Win32API.MouseMoveTo(x, y)  
    except Exception as e:
        raise e


def set_text(win_title=None,id=None,text=None,waitfor=WAIT_FOR,run_mode='noctrl'):
    """sap 设置文本"""
    try:
        __logger.debug('sap set text :'+str(id))
        if (win_title != None):
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)
        element = get_element(id, waitfor) 
        text = encrypt.decrypt(str(text))
        element.text = text
    except Exception as e:
        raise e


def get_text(win_title=None,id=None,row=None,col=None,waitfor=WAIT_FOR):
    """sap 获取文本"""
    try:
        __logger.debug('sap get text :' + str(id))
        if (win_title != None):
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)
        element = get_element(id, waitfor)
        if row != None and col != None and element.type == 'GuiShell':
            text = element.GetCellValue(row, col)
        else:
            text = element.text
        return text
    except Exception as e:
        raise e


def get_select_items(win_title=None,id=None,waitfor=WAIT_FOR):
    """sap 得到下拉框全部选项"""
    try:
        __logger.debug('sap get select items :' + str(id))
        if (win_title != None):
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)
        element = get_element(id, waitfor)
        pass
    except Exception as e:
        raise e


def get_selected_item(win_title=None,id=None,waitfor=WAIT_FOR):
    """sap 得到下拉框当前选项"""
    try:
        __logger.debug('sap get selected item :' + str(id))
        if (win_title != None):
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)
        element = get_element(id, waitfor)
        item_text = element.value
        return item_text
    except Exception as e:
        raise e


def set_select_item(win_title=None,id=None,item_text='',waitfor=WAIT_FOR):
    """sap 设置下拉框值"""
    try:
        __logger.debug('sap set select item :' + str(id))
        if (win_title != None):
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)
        element = get_element(id, waitfor)
        element.value = item_text

    except Exception as e:
        raise e


def do_check(win_title=None,id=None,action="check",waitfor=WAIT_FOR):
    """sap checkbox"""
    try:
        __logger.debug('sap do check :' + str(id))
        if (win_title != None):
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)
        element = get_element(id, waitfor)
        if action == "check":
            element.selected = -1
        else:
            element.selected = 0

    except Exception as e:
        raise e


def get_cell_value(win_title=None,id="",row =None,col =None,waitfor=WAIT_FOR):
    """sap shell表单获取单元格值"""
    try:
        __logger.debug('sap get cell value :' + str(id))
        if (win_title != None):
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)
        element = get_element(id, waitfor)
        cellvalue = element.GetCellValue(row, col)
        return cellvalue
    except Exception as e:
        raise e


def get_column_value(win_title=None,id="",col=None,waitfor=WAIT_FOR):
    """sap shell表单获取整列"""
    try:
        __logger.debug('sap get column value :' + str(id))
        if (win_title != None):
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)
        element = get_element(id, waitfor)
        tableRowCount = element.RowCount
        column_list = []
        for i in range(tableRowCount):
            cellvalue = element.GetCellValue(i, col)
            column_list.append(cellvalue)
        return column_list
    except Exception as e:
        raise e

def get_row_value(win_title=None,id="",row=None,waitfor=WAIT_FOR):
    """sap shell表单获取整行"""
    try:
        __logger.debug('sap get row value :' + str(id))
        if (win_title != None):
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)
        element = get_element(id, waitfor)
        tableColumnCount = element.ColumnCount
        print(tableColumnCount)
        row_list = []
        for i in range(tableColumnCount):
            cellvalue = element.GetCellValue(row, i)
            row_list.append(cellvalue)
        print(row_list)
        return row_list
    except Exception as e:
        raise e


def __get_sap_element(path):

    try:
        id_str = path.split("/",5)
        con = int(id_str[2][4:-1])
        ses = int(id_str[3][4:-1])
        wnd = int(id_str[4][4:-1])
        id = id_str[5]
        return (con, ses, wnd,id)
    except Exception as e:
        raise e

def get_element(id,waitfor):  
    __logger.debug('sap get element : ['+str(id)+']')  
    try:
        conn,sess,win,id = __get_sap_element(id)
        sc = SapControl(conn,sess,win)
        starttime = time.time()
        while True:
            try:
                element = sc.findElement(id) 
                return element
            except Exception as e:
                runtime = time.time() - starttime
                if runtime >= waitfor:                    
                    raise Exception('sap get text element not found :[' + str(id) + ']') 
                time.sleep(TRY_INTERVAL)  
    except Exception as e:
        raise e 
    

def __get_element_pos(id=None,row=None,col=None,curson='center',offsetX=0,offsetY=0,waitfor=WAIT_FOR):
    X = None
    Y = None 
    try: 
        element = get_element(id, waitfor) 
        left = element.screenLeft
        top = element.screenTop
        width = element.width
        height = element.height
        if row!=None and col!=None and element.type=='GuiShell':
            left = left+element.getCellLeft(row,col)
            top = top+element.getCellTop(row,col)
            width = element.GetCellWidth(row,col)
            height = element.GetCellHeight(row,col)
        curs = str(curson).lower()
        if curs == "center":
            X = left + width/2 + offsetX
            Y = top + height/2 + offsetY
        if curs == "lefttop":
            X = left + offsetX
            Y = top + offsetY
        if curs == "righttop":
            X = left + width + offsetX
            Y = top + offsetY
        if curs == "leftbottom":
            X = left + offsetX
            Y = top + height + offsetY
        if curs == "rightbottom":
            X = left + width + offsetX
            Y = top + height + offsetY
        dll = cdll.LoadLibrary("../../bin/ScreenScaling.dll")
        scal = dll.GetScreenScaling()/100
        return int(X/scal),int(Y/scal)
    except Exception as e:
        raise e

def get_element_rect(id=None, row=None,col=None,curson='lefttop',offsetX=0,offsetY=0,waitfor=WAIT_FOR):

    try:
        element = get_element(id, waitfor)
        left = element.screenLeft
        top = element.screenTop
        width = element.width
        height = element.height

        if curson != None and curson != "":

            curson_x, curson_y = __get_element_pos(id=id, row=row,col=col,curson=curson, offsetX=offsetX, offsetY=offsetY)
            return curson_x, curson_y, width, height
        else:
            return left,top,width,height
    except Exception as e:
        raise e


def capture_element_img(win_title=None,in_img_path=None, id=None,row=None,col=None,waitfor=WAIT_FOR):

    try:
        curson_x, curson_y, width, height = get_element_rect(id=id, row=row,col=col,curson='lefttop')

        in_img_path = img.capture_image(win_title=win_title, win_text='',in_img_path=in_img_path,left_indent=curson_x, top_indent=curson_y, width=width, height=height,waitfor=waitfor)
        return in_img_path
    except Exception as e:
        raise e

