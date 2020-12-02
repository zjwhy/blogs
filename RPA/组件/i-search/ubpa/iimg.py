# -*- coding: utf-8 -*-
'''
Created on 2018。3.29

@author: Wu.Xin

图片相关处理
'''
from ctypes import *
import datetime
import json
import random
import string
import time
import traceback
from ubpa.iconstant import *
from ubpa.ilog import ILog 

from PIL import Image, ImageGrab

import aircv as ac
import ubpa.base_native_ait as nit
import ubpa.ics as ics 
import ubpa.ierror as error
import ubpa.iwin as iwin


dll = cdll.LoadLibrary("../../bin/ScreenScaling.dll")
capture_dll = cdll.LoadLibrary("../../bin/Screenshots.dll")

# capture_dll = cdll.LoadLibrary(r"d:\svn\isa\branches\ueba_5.0\makesetup\CdaSetupDate\bin\Screenshots.dll")

__logger = ILog(__file__)


def get_scale():
    '''
    获取屏幕缩放比例
    '''    
    return dll.GetScreenScaling()


def screen_capture(img_path):
    '''
    截取屏幕
    '''
    capture_dll.ScreenshotsToFile(img_path)
    
 

def get_cv_confidence_percent(confidence): 
    '''
     获取识别信心百分比   [5, 9]
    '''  
    if confidence[1] < 8 :
        __logger.debug(u"Confidence is lower than reference point:"+str(confidence))
    return confidence[0]/confidence[1]




    
def cal_position(centerpos,rectangle,pos_curson="Center",pos_offsetY=0,pos_offsetX=0):
    '''
    根据传入的值计算位置
    '''
    pos = None
    sc = get_scale()/100
    __logger.debug(u"scaling is:"+str(sc))
    if pos_curson == 'Center':
        pos = centerpos
    elif pos_curson == 'TopLeft':
        pos = rectangle[0]    
    elif pos_curson == 'TopRight':
        pos = rectangle[3]
    elif pos_curson == 'BottomLeft':
        pos = rectangle[1]
    elif pos_curson == 'BottomRight':
        pos = rectangle[2]
    
    if pos != None: 
        pos[0] = pos[0]
        pos[1] = pos[1]
        __logger.debug(u"position before compute:"+str(pos))
        pos[0] = pos[0]/sc+pos_offsetX
        pos[1] = pos[1]/sc+pos_offsetY 
        __logger.debug(u"position after compute:"+str(pos))
        
    return pos 


def get_image_cv_pos(img_res_path=None,image=None,pos_curson="Center",pos_offsetY=0,pos_offsetX=0,confidence_df=0.85,waitfor=WAIT_FOR_IMG):
    '''
    截屏并根据图片计算其位置
    '''  
    __logger.debug(r'ready OpenCV Recognition operation') 
    pos = None  
    try:
        starttime = time.time()
        image = img_res_path + '\\res\\' + image
        while True:
            try: 
                pic = TEMP_PATH+'ScreenCapture.png'
                screen_capture(pic)
                imsrc = ac.imread(pic) # 原始图像
                imsch = ac.imread(image)
#                 imsch = ac.imread('d:/1.png') # 带查找的部分 
#                 print(str(ac.sift_count(r'd:\1.png')))
                sift_json = ac.find_sift(imsrc, imsch)  
                if sift_json==None: 
                    print(u'sift_json return null，OpenCV cannot recognize picture')
                else : 
                    sift_dict = json.loads(json.dumps(sift_json)) 
                    __logger.warning(u'OpenCV Identifying return information  :'+str(sift_dict))
                    #误取信心度
                    confidence = get_cv_confidence_percent(sift_dict['confidence']) 
                    if confidence >= confidence_df:
                        #根据相关信息计算真正位置
                        pos = cal_position(sift_dict['result'],sift_dict['rectangle'],pos_curson,pos_offsetY,pos_offsetX)
                        if pos[0]<0 or pos[1] <0 :
                            __logger.debug(u'Location information is negative, error')
                            pos = None
                            continue
                        __logger.warning(u'OpenCV confidence :'+str(confidence))
                        break
                    else :
                        __logger.error(u'OpenCV confidence too low:'+str(confidence))
            except Exception as ex:
                print(str(ex),traceback.format_exc())
                pass
         
            runtime = time.time() - starttime
            if runtime >= waitfor:
                break
            __logger.debug(r'OpenCV Recognize failure and wait for the next time ')
            time.sleep(TRY_INTERVAL)
    except Exception as e:
        print(str(e),traceback.format_exc())
    finally:
        return pos


'''
图片点击  包含单击和双击  此方法共用
'''
def img_click_au3(win_title=None, img_res_path=None, image=None, mouse_button="left", pos_curson="Center",
                  pos_offsetY=0, pos_offsetX=0,times=1, image_size=None, waitfor=WAIT_FOR_IMG):
    __logger.debug(u"Ready to execute[img_click]")

    try:
        '''如果屏幕缩放比例不是100%'''
        if not __check_scale():
            __logger.warning(u"Waring:The current screen zoom ratio is not 100%. Picture lookup may not be accurate.")

        ''''如果指定窗口'''
        if win_title != None and win_title.strip() != '':
            ''''如果窗口不活跃状态'''
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)

        msg = get_img_cli_au3(img_res_path, image, mouse_button, pos_curson, pos_offsetY, pos_offsetX, image_size,
                              waitfor, times, 1)

        tmp_au3_file_path = nit.gen_au3_file(msg)

        status, error_string, stdout_string = nit.run_autoit(tmp_au3_file_path)
        nit.cleanup(tmp_au3_file_path)
        if status:
            '''程序执行错误'''
            __logger.error("Au3program execution error")
            return False
        elif str(nit.get_cmd_message(stdout_string)) == "NO":
            '''autoit 执行返回结果为未找到'''
            __logger.error("ImageSearch image not found")
            return False
        return True
    except Exception as e:
        print(str(e), traceback.format_exc())
        return False
    finally:
        __logger.debug(u"end execute[img_click]")

'''
图片点击  包含单击和双击  此方法共用
'''
def img_click_cv(win_title=None, img_res_path=None, image=None, mouse_button="left", pos_curson="Center", pos_offsetY=0,
                 pos_offsetX=0,times=1,confidence=0.85, waitfor=WAIT_FOR_IMG):
    '''
    使用aircv  opencv 进行图片查找匹配，并单击位置
    '''
    try:
        pos = get_image_cv_pos(img_res_path, image, pos_curson, pos_offsetY, pos_offsetX,confidence ,waitfor)
        if pos == None:
            __logger.error('OpenCv Image Not Found')
            return False
        else:
            # 鼠标单击
            ics.mouse_click(win_title, pos[0], pos[1], mouse_button, times, waitfor)
            return True
    except Exception as e:
        print(str(e), traceback.format_exc())


def img_click(win_title=None,img_res_path=None,image=None,mouse_button="left",pos_curson="Center",pos_offsetY=0,pos_offsetX=0,
              image_size=None,waitfor=WAIT_FOR_IMG):
    '''
    图片单击,支持全图片，opencv
    '''
    __logger.debug(r'Prepare to click Recognition Picture') 
    try:
        starttime = time.time() 
        while True:
            ''' 先使用ImageSearch查找  '''
            flg = img_click_au3(win_title,img_res_path,image,mouse_button,pos_curson,pos_offsetY,pos_offsetX,1,image_size,waitfor=1)

            if not flg :
                ''' 使用OpenCv查找点击''' 
                __logger.debug(r'ImageSearch Unmistakable, OpenCV Recognition ')
                flg =  img_click_cv(win_title,img_res_path,image,mouse_button,pos_curson,pos_offsetY,pos_offsetX,1,waitfor=1)
            
            if flg :
                break
            
            runtime = time.time() - starttime
            if runtime >= waitfor:
                raise error.ImageNotFoundError('Image Not Found')
            
            __logger.debug(r'Picture Failure, Waiting for Next Recognition ')
            time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[img_dbclick]")
    

def img_dbclick(win_title=None,img_res_path=None,image=None,mouse_button="left",pos_curson="Center",pos_offsetY=0,pos_offsetX=0,
                image_size=None,waitfor=WAIT_FOR_IMG):
    '''
    图片双击,支持全图片，opencv
    '''
    __logger.debug(r'Prepare double-click recognition picture')
    try:
        starttime = time.time() 
        while True:
            ''' 先使用ImageSearch查找  '''
            flg = img_click_au3(win_title,img_res_path,image,mouse_button,pos_curson,pos_offsetY,pos_offsetX,2,image_size,waitfor=1)
            
            if not flg :
                ''' 使用OpenCv查找点击''' 
                __logger.debug(r'ImageSearch Unmistakable, OpenCV Recognition ')
                flg =  img_click_cv(win_title,img_res_path,image,mouse_button,pos_curson,pos_offsetY,pos_offsetX,2,waitfor=1)
            
            if flg :
                break
            
            runtime = time.time() - starttime
            if runtime >= waitfor:
                raise error.ImageNotFoundError('Image Not Found')
            
            __logger.debug(r'Picture Failure, Waiting for Next Recognition ')
            time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[img_dbclick]")


'''
图片点击 单击和双击的共用 比img_click，img_dbclick多了一个参数times  
'''
def do_click_pos(win_title=None, img_res_path=None, image=None, button="left", curson="Center", offsetX=0, offsetY=0,
             times=1, image_size=None,fuzzy=True, confidence=0.85,waitfor=WAIT_FOR_IMG):
    '''
    图片单击,支持全图片，opencv
    '''
    __logger.debug(r'Ready to identify pictures.')
    try:
        starttime = time.time()
        while True:
            ''' 先使用ImageSearch查找  '''
            flg = img_click_au3(win_title,img_res_path,image,button,curson,offsetY,offsetX,times,image_size,waitfor=1)

            if (not flg) and fuzzy:
                ''' 使用OpenCv查找点击'''
                __logger.debug(r'ImageSearch Unmistakable, OpenCV Recognition ')
                flg = img_click_cv(win_title,img_res_path,image,button,curson,offsetY,offsetX,times,confidence,waitfor=1)

            if flg:
                break

            runtime = time.time() - starttime
            if runtime >= waitfor:
                raise error.ImageNotFoundError('Image Not Found')

            __logger.debug(r'Picture Failure, Waiting for Next Recognition ')
            time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[do_click_pos]")


def img_exists(win_title=None,img_res_path=None,image=None,fuzzy=True,confidence=0.85,waitfor=WAIT_FOR_IMG):
    '''图片是否存在'''
    is_exists = True 
    __logger.debug(r'Ready img_exists ')
    try:
        starttime = time.time() 
        while True:
            ''' 先使用ImageSearch查找  '''
            is_exists = img_exists_au3(win_title,img_res_path,image,waitfor=1) 
            if (not is_exists) and fuzzy:
                ''' 使用OpenCv查找点击''' 
                __logger.debug(r'ImageSearch Unmistakable, OpenCV Recognition ') 
                
                is_exists =  img_exists_cv(win_title=win_title,img_res_path=img_res_path,image=image,confidence=confidence,waitfor=1)
            
            if is_exists :
                break
            
            runtime = time.time() - starttime
            if runtime >= waitfor:
                raise error.ImageNotFoundError('Image Not Found')
            
            __logger.debug(r'Picture Failure, Waiting for Next Recognition ')
            time.sleep(TRY_INTERVAL)
    except Exception as e:
        pass
    finally:
        __logger.debug(u"end execute[img_exists]" + str(is_exists))
        return is_exists
    

def img_exists_au3(win_title=None,img_res_path=None,image=None,waitfor=WAIT_FOR_IMG):

    __logger.debug(u"Ready to execute[img_exists]")
    is_exists = False

    try:
        ''''如果指定窗口'''
        if win_title != None and win_title.strip() != '':
            ''''如果窗口不活跃状态'''
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)

        msg = get_img_exist_au3(img_res_path, image, waitfor)

        tmp_au3_file_path = nit.gen_au3_file(msg)

        status, error_string, stdout_string = nit.run_autoit(tmp_au3_file_path)
        nit.cleanup(tmp_au3_file_path)
        if status:
            '''program execution error'''
            __logger.error("aitprogram execution error")
            return False 
        elif str(nit.get_cmd_message(stdout_string)) == "NO":
            '''autoit 执行返回结果为未找到'''
            __logger.error("ImageSearch image not found") 
            return False

        return True
    except Exception as e: 
        print(str(e),traceback.format_exc())
    finally:
        __logger.debug(u"au3end execute[img_exists]" + str(is_exists))


def img_exists_cv(win_title=None,img_res_path=None,image=None,mouse_button="left",pos_curson="Center",pos_offsetY=0,pos_offsetX=0,confidence=0.85,
                  waitfor=WAIT_FOR_IMG):
    '''
    使用aircv  opencv 进行图片是否存在
    '''
    try:
       pos = get_image_cv_pos(img_res_path,image,pos_curson,pos_offsetY,pos_offsetX,confidence,waitfor)
       if pos == None:
           return False
       else:
           return True
    except Exception as e:
        print(str(e),traceback.format_exc())
    


def img_moveto(win_title=None,img_res_path=None,image=None,mouse_button="left",pos_curson="Center",pos_offsetY=0,pos_offsetX=0,
               image_size=None,waitfor=WAIT_FOR_IMG):
    '''
    图片移动,支持全图片，opencv
    '''
    __logger.debug(r'Ready to move to the picture')
    try:
        starttime = time.time() 
        while True:
            ''' 先使用ImageSearch查找  '''
            flg = img_moveto_au3(win_title,img_res_path,image,mouse_button,pos_curson,pos_offsetY,pos_offsetX,image_size,waitfor=1)
            
            if not flg :
                ''' 使用OpenCv查找点击''' 
                __logger.debug(r'ImageSearch Unmistakable, OpenCV Recognition ')
                flg =  img_moveto_cv(win_title,img_res_path,image,mouse_button,pos_curson,pos_offsetY,pos_offsetX,waitfor=1)
            
            if flg :
                break
            
            runtime = time.time() - starttime
            if runtime >= waitfor:
                raise error.ImageNotFoundError('Image Not Found')
            
            __logger.debug(r'Picture Failure, Waiting for Next Recognition ')
            time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[img_moveto]")
        
def do_moveto_pos(win_title=None,img_res_path=None,image=None,curson='center',offsetX=0,offsetY=0,image_size=None,fuzzy=True, confidence=0.85,waitfor=30):
    '''
        图片移动,支持全图片，opencv
        '''
    __logger.debug(r'Ready execute [do_moveto_pos]')
    try:
        starttime = time.time()
        while True:
            ''' 先使用ImageSearch查找  '''
            flg = img_moveto_au3(win_title, img_res_path, image, "", curson, offsetY, offsetX, image_size,waitfor=1)

            if (not flg)and fuzzy:
                ''' 使用OpenCv查找点击'''
                __logger.debug(r'ImageSearch Unmistakable, OpenCV Recognition ')
                flg = img_moveto_cv(win_title, img_res_path, image, "", curson, offsetY, offsetX, confidence ,waitfor=1)

            if flg:
                break

            runtime = time.time() - starttime
            if runtime >= waitfor:
                raise error.ImageNotFoundError('Image Not Found')

            __logger.debug(r'Picture Failure, Waiting for Next Recognition ')
            time.sleep(TRY_INTERVAL)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[do_moveto_pos]")
    

def img_moveto_au3(win_title=None,img_res_path=None,image=None,mouse_button="left",pos_curson="Center",pos_offsetY=0,pos_offsetX=0,
                   image_size=None,waitfor=WAIT_FOR_IMG):

    __logger.debug(u"Ready to execute[img_move]")

    try:
        '''如果屏幕缩放比例不是100%'''
        if not __check_scale():
            __logger.warning(u"Waring:The current screen zoom ratio is not 100%. Picture lookup may not be accurate.")

        ''''如果指定窗口'''
        if win_title != None and win_title.strip() != '':
            ''''如果窗口不活跃状态'''
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)
        msg = get_img_cli_au3(img_res_path, image, mouse_button, pos_curson, pos_offsetY, pos_offsetX, image_size, waitfor,1, 0)

        tmp_au3_file_path = nit.gen_au3_file(msg)

        status, error_string, stdout_string = nit.run_autoit(tmp_au3_file_path)
        nit.cleanup(tmp_au3_file_path)
        if status:
            '''program execution error'''
            __logger.error("aitprogram execution error")
            return False

        elif str(nit.get_cmd_message(stdout_string)) == "NO":
            '''autoit 执行返回结果为未找到'''
            __logger.error("image not found")
            return False 
        return True
    except Exception as e:
        print(str(e),traceback.format_exc())
    finally:
        __logger.debug(u"end execute[img_move]")



def img_moveto_cv(win_title=None,img_res_path=None,image=None,mouse_button="left",pos_curson="Center",pos_offsetY=0,pos_offsetX=0,confidence_df=0.85,waitfor=WAIT_FOR_IMG):
    '''
    使用aircv  opencv 进行图片查找位置，并移动位置
    '''
    try:
       pos = get_image_cv_pos(img_res_path,image,pos_curson,pos_offsetY,pos_offsetX,confidence_df,waitfor)
       if pos == None:
           __logger.error('OpenCv Image Not Found')
           return False
       else:
           #鼠标移动
           ics.mouse_moveto(win_title,pos[0],pos[1],waitfor)
           return True
    except Exception as e:
        print(str(e),traceback.format_exc())
    
    

def capture_image(win_title = "", win_text = "", in_img_path = None, left_indent = 0, top_indent = 0, width = 0, height = 0,waitfor=WAIT_FOR_IMG):
    __logger.echo_msg(u"Ready to execute[capture_image]")

    try:
        '''如果屏幕缩放比例不是100%'''
        if not __check_scale():
            __logger.warning(u"Waring:The current screen zoom ratio is not 100%. Picture lookup may not be accurate.")

        ''''如果指定窗口'''
        if win_title != None and win_title.strip() != '':
            ''''如果窗口不活跃状态'''
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)

        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))

        if in_img_path == None: # 当没有输入路径的时候
            capture_image_path = nit.set_au3_file_res_path(__file__)
            in_img_path = capture_image_path + "\\temp\\" + ran_str + ".png"
        else:
            in_img_path = in_img_path + ran_str + ".png"

        right_indent = left_indent + width
        bottom_indent = top_indent + height
        
        bbox = (left_indent,top_indent,right_indent,bottom_indent)
        im = ImageGrab.grab(bbox)
        im.save(in_img_path)
        return in_img_path
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[capture_image]")


def move_to_move(win_title="",x=0,y=0,str_xy="",waitfor=WAIT_FOR_IMG):
    __logger.debug(u"Ready to execute[move_to_move]")

    try:
        ''''如果指定窗口'''
        if win_title != None and win_title.strip() != '':
            ''''如果窗口不活跃状态'''
            if not iwin.do_win_is_active(win_title):
                iwin.do_win_activate(win_title=win_title, waitfor=waitfor)

        msg = move_to_move_pack_au3(x, y, str_xy)

        tmp_au3_file_path = nit.gen_au3_file(msg)

        print(tmp_au3_file_path)

        status, error_string, stdout_string = nit.run_autoit(tmp_au3_file_path)
        nit.cleanup(tmp_au3_file_path)
        if status:
            '''程序执行错误'''
            __logger.error("aitprogram execution error")
            return False

        elif str(nit.get_cmd_message(stdout_string)) == "NO":
            '''autoit 执行返回结果为未找到'''
            __logger.error("move failure")
            return False
        return True
    except Exception as e:
        print(str(e), traceback.format_exc())
    finally:
        __logger.debug(u"end execute[move_to_move]")


def move_to_move_pack_au3(x1, y1, str_xy):

    str_xy_list = str_xy.split(",")
    pre_msg = "#include <AutoItConstants.au3>" \
              + '\n' + "MouseMove(" + str(x1) + "," + str(y1) + ")" \
              + '\n' + "Opt('MouseClickDownDelay', 50000)" \
              + '\n' + "MouseDown($MOUSE_CLICK_LEFT)"
    for index in str_xy_list:
        pos = index.split(".")
        x = pos[0]
        y = pos[1]
        pre_msg = pre_msg + '\n' + "MouseMove(" + x + "," + y + ")" \
                  + '\n' + "Sleep(500)"

    pre_msg = pre_msg + '\n' + "MouseUp($MOUSE_CLICK_LEFT)"

    return pre_msg


def __check_scale():
    '''
检测缩放比例  100%  0...表示缩放比例不是100%   1....表示缩放比例等于100%
    '''
    return dll.IsHundredPercent()



#pos_curson 点的位置 中间，左上，右上，左下，右下
#pox_offsetX X偏移量
#pos_offsetY Y偏移量
#waitfor 等待时间
def get_img_cli_au3(img_res_path,image,mouse_button,pos_curson,pos_offsetY,pos_offsetX,image_size,waitfor,mode,flag):

    image = img_res_path + '\\res\\' + image
    sc = get_scale()/100
    if image_size == None:  # 图片大小 #68X19
        img = Image.open(image) # 获取图片大小
        X = img.size[0]/sc
        Y = img.size[1]/sc
    else:
        image_size = image_size.split('X')
        X = float(image_size[0])/sc
        Y = float(image_size[1])/sc
    if pos_curson == "Center":
        x = "$x+" + str(int(X) / 2) + "+" + str(pos_offsetX)
        y = "$y+" + str(int(Y) / 2) + "+" + str(pos_offsetY)
    if pos_curson == "TopLeft":
        x = "$x+" + str(pos_offsetX)
        y = "$y+" + str(pos_offsetY)
    if pos_curson == "TopRight":
        x = "$x+" + str(X) + "+" + str(pos_offsetX)
        y = "$y+" + str(pos_offsetY)
    if pos_curson == "BottomLeft":
        x = "$x+" + str(pos_offsetX)
        y = "$y+" + str(Y) + "+" + str(pos_offsetY)
    if pos_curson == "BottomRight":
        x = "$x+" + str(X) + "+" + str(pos_offsetX)
        y = "$y+" + str(Y) + "+" + str(pos_offsetY)

    if flag == 1:
        mid_msg = "   MouseClick('" + mouse_button + "'," + x + "," + y + "," + str(mode) + ",10)"
    else:
        mid_msg = "   MouseMove(" + x + "," + y + ",10)"

    pre_msg = "#include <ImageSearch.au3>" \
              + '\n' + "$x=0" \
              + '\n' + "$y=0" \
              + '\n' + "#PRE_Change2CUI=y" \
              + '\n' + "$result = _WaitForImageSearch('" + image + "'," + str(waitfor) + ",0,$x,$y,0)" \
              + '\n' + 'if $result=1 Then'

    suf_msg = "   ConsoleWrite('OK')" \
              + '\n' + 'Else' \
              + '\n' + '   ConsoleWrite("NO")' \
              + '\n' + 'EndIf'

    msg = pre_msg + '\n' + mid_msg + '\n' + suf_msg
    return msg


def get_img_exist_au3(img_res_path=None,image=None,waitfor=30):
    image = img_res_path + '\\res\\' + image

    pre_msg = "#include <ImageSearch.au3>" \
              + '\n' + "$x=0" \
              + '\n' + "$y=0" \
              + '\n' + "#PRE_Change2CUI=y" \
              + '\n' + "$result = _WaitForImageSearch('" + image + "'," + str(waitfor) + ",0,$x,$y,10)" \
              + '\n' + 'if $result=1 Then'

    suf_msg = "   ConsoleWrite('OK')" \
              + '\n' + 'Else' \
              + '\n' + '   ConsoleWrite("NO")' \
              + '\n' + 'EndIf'

    msg = pre_msg + '\n' + '\n' + suf_msg
    return msg

def get_img_capture_au3(out_img_path,left_indent, top_indent, right_indent, bottom_indent):

    pre_msg =  "#include <Tesseract.au3>" \
            + '\n' + "Global $capture_filename = " + out_img_path \
            + '\n' + "CaptureToTIFF('', '', '', $capture_filename, 1, " +str(left_indent)+ "," +str(top_indent)+ "," +str(right_indent)+ "," +str(bottom_indent)+ ")"

    return pre_msg






