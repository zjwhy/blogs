# -*- coding: utf-8 -*-
import os
from time import ctime, sleep
import datetime
import sys
import json
from ubpa.base_native_ait import *
import random
import string
from PIL import Image
import traceback

from ubpa.ilog import ILog
from ubpa.iresult import IResult

__logger = ILog(__file__)


def img_click(img_res_path, param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[img_click]")

    iresult = IResult()
    msg = cli_pack_au3(img_res_path, param, 1,1)  ##组装生成au3所需的数据
    try:
        tmp_au3_file_path = gen_au3(img_res_path, msg)  # 生成XXX.au3文件并返回路径

        status, error_string, stdout_string = run_autoit(tmp_au3_file_path)

        if status:
            '''程序执行错误'''
            iresult.status = 1
            iresult.err = get_cmd_message(error_string)
            raise Exception(iresult.err)
        elif str(get_cmd_message(stdout_string)) == "NO":
            '''autoit 执行返回结果为未找到'''
            iresult.status = 1
            iresult.err = u'image not found'
            raise Exception(iresult.err)

        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __cleanup(tmp_au3_file_path)
        __logger.echo_msg(u"end execute[img_click]")

def img_dbclick(img_res_path, param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[img_dbclick]")

    iresult = IResult()
    msg = cli_pack_au3(img_res_path, param, 2,1)
    try:
        tmp_au3_file_path = gen_au3(img_res_path, msg)

        status, error_string, stdout_string = run_autoit(tmp_au3_file_path)

        if status:
            '''程序执行错误'''
            iresult.status = 1
            iresult.err = get_cmd_message(error_string)
            raise Exception(iresult.err)
        elif str(get_cmd_message(stdout_string)) == "NO":
            '''autoit 执行返回结果为未找到'''
            iresult.status = 1
            iresult.err = u'image not found'
            raise Exception(iresult.err)

        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __cleanup(tmp_au3_file_path)
        __logger.echo_msg(u"end execute[img_dbclick]")



def img_exists(img_res_path, param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[img_exists]")

    iresult = IResult()
    msg = is_exist_pack_au3(img_res_path, param)
    try:
        tmp_au3_file_path = gen_au3(img_res_path, msg)
        status, error_string, stdout_string = run_autoit(tmp_au3_file_path)
        iresult.obj = True
        if status:
            '''程序执行错误'''
            iresult.status = 1
            iresult.err = get_cmd_message(error_string)
            iresult.obj = False
        elif str(get_cmd_message(stdout_string)) == "NO":
            '''autoit 执行返回结果为未找到'''
            iresult.status = 1
            iresult.err = u'image not found'
            iresult.obj = False

        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __cleanup(tmp_au3_file_path)
        __logger.echo_msg(u"end execute[img_exists]")


def img_move(img_res_path, param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[img_move]")

    iresult = IResult()
    msg = cli_pack_au3(img_res_path, param, 1, 0)
    try:
        tmp_au3_file_path = gen_au3(img_res_path, msg)
        status, error_string, stdout_string = run_autoit(tmp_au3_file_path)

        if status:
            '''程序执行错误'''
            iresult.status = 1
            iresult.err = get_cmd_message(error_string)
            raise Exception(iresult.err)
        elif str(get_cmd_message(stdout_string)) == "NO":
            '''autoit 执行返回结果为未找到'''
            iresult.status = 1
            iresult.err = u'image not found'
            raise Exception(iresult.err)

        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __cleanup(tmp_au3_file_path)
        __logger.echo_msg(u"end execute[img_move]")


def capture_image(win_title = "", win_text = "", in_img_path = "", left_indent = 0, top_indent = 0, width = 0, height = 0):
    __logger.info(u"Afferent parameter:left_indent:" + str(left_indent) + ",top_indent:" + str(top_indent) + ",width:" + str(width) + ",height:" + str(height))
    __logger.echo_msg(u"Ready to execute[capture_image]")

    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))

    if in_img_path == "": # 当没有输入路径的时候
        in_img_path = tempfile.mktemp(prefix='tm_')
        in_img_path = in_img_path + ran_str + ".png"
        in_img_path = in_img_path.replace("\\", "\\\\")
    else:
        in_img_path = in_img_path + ran_str + ".png"

    iresult = IResult()
    right_indent = left_indent + width
    bottom_indent = top_indent + height
    msg = img_capture_pack_au3("'" +in_img_path+ "'",left_indent, top_indent, right_indent, bottom_indent)
    try:
        tmp_au3_file_path = gen_au3_file(msg)
        status, error_string, stdout_string = run_autoit(tmp_au3_file_path)

        iresult.obj = in_img_path
        if status != 0:
            '''程序执行错误'''
            iresult.status = 1
            iresult.err = get_cmd_message(error_string)
            raise Exception(iresult.err)

        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __cleanup(tmp_au3_file_path)
        __logger.echo_msg(u"end execute[capture_image]")


def set_img_res_path(pfile):
    img_res_path = os.path.abspath(os.path.join(os.path.dirname(pfile), ".."));
    return img_res_path


def gen_au3(img_res_path, params):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    au3_file_name = img_res_path + os.sep + ran_str + ".au3"
    try:
        au3_file = open(au3_file_name, 'w')
        au3_file.write(params)
    finally:
        if au3_file:
            au3_file.close()
        return au3_file_name

def set_au3_file_res_path(pfile):
    img_res_path = os.path.abspath(os.path.join(os.path.dirname(pfile), "../../../.."));
    return img_res_path

def gen_au3_file(params):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    au3_file_res_path = set_au3_file_res_path(__file__)
    au3_file_name = au3_file_res_path + "\\studio\\" + ran_str + ".au3"
    try:
        au3_file = open(au3_file_name, 'w')
        au3_file.write(params)
    finally:
        if au3_file:
            au3_file.close()
        return au3_file_name


def __cleanup(temp_name):
    ''' Tries to remove files by filename wildcard path. '''
    for filename in iglob(temp_name + '*'):
        try:
            os.remove(filename)
        except OSError:
            pass


def cli_pack_au3(img_res_path, param, mode,flag):
    paramJason = json.loads(param)
    target = paramJason.get("target")
    image = target["image"]
    image = img_res_path + '\\res\\' + image  #D:\robotTool2\studio\project_20180312092920218\res\snapshot_20180312133718403.png
    image_size = target["image_size"]  # 图片大小 #68X19
    if image_size == "":
        img = Image.open(image) # 获取图片大小
        X = img.size[0]
        Y = img.size[1]
    else:
        image_size = image_size.split('X')
        X = image_size[0]
        Y = image_size[1]

    input = paramJason.get("input")
    mouse_button = input.get("mouse_button", "")
    pos_curson = input["pos_curson"]  # 点的位置 中间，左上，右上，左下，右下
    pox_offsetX = input.get('pox_offsetX', "")  # X偏移量
    pos_offsetY = input.get('pos_offsetY', "")  # Y偏移量
    waitfor = input.get('waitfor', "")  # 等待时间

    if pos_curson == "Center":
        x = "$x+" + str(int(X) / 2) + "+" + pox_offsetX
        y = "$y+" + str(int(Y) / 2) + "+" + pos_offsetY
    if pos_curson == "TopLeft":
        x = "$x+" + pox_offsetX
        y = "$y+" + pos_offsetY
    if pos_curson == "TopRight":
        x = "$x+" + str(X) + "+" + pox_offsetX
        y = "$y+" + pos_offsetY
    if pos_curson == "BottomLeft":
        x = "$x+" + pox_offsetX
        y = "$y+" + str(Y) + "+" + pos_offsetY
    if pos_curson == "BottomRight":
        x = "$x+" + str(X) + "+" + pox_offsetX
        y = "$y+" + str(Y) + "+" + pos_offsetY

    if flag == 1:
        mid_msg = "   MouseClick('" + mouse_button + "'," + x + "," + y + "," + str(mode) + ",0)"
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


def is_exist_pack_au3(img_res_path, param):
    paramJason = json.loads(param)
    target = paramJason.get("target")
    image = target["image"]
    image = img_res_path + '\\res\\' + image

    input = paramJason.get("input")
    waitfor = input.get('waitfor', "")  # 等待时间

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

    msg = pre_msg + '\n' + '\n' + suf_msg
    return msg

def img_capture_pack_au3(out_img_path,left_indent, top_indent, right_indent, bottom_indent):

    pre_msg =  "#include <Tesseract.au3>" \
            + '\n' + "Global $capture_filename = " + out_img_path \
            + '\n' + "CaptureToTIFF('', '', '', $capture_filename, 1, " +str(left_indent)+ "," +str(top_indent)+ "," +str(right_indent)+ "," +str(bottom_indent)+ ")"

    return pre_msg


