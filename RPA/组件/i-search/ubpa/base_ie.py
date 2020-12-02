# -*- coding: utf-8 -*-
from ctypes import *
import datetime
import json
from ubpa.ilog import ILog
from ubpa.iresult import IResult
import traceback
import time

print("begin")
dll = cdll.LoadLibrary("../../bin/UEBAIEWatcher.dll")
__try_times = 2

__logger = ILog(__file__)

def getText(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[getText]")

    iresult = IResult()  # new一个返回结果的新对象
    iresult.status = 0  # status初始赋值   status =0 成功  1 表示失败

    try:
        stringText = get_text(param) #取得getText方法返回值
        stringRst = check_is_wrong() #判断getText方法是否成功

        if stringRst != "":#表示报错了

            for le in range(0,__try_times):
                __logger.info(str((le+1))+"times,"+"Afferent parameter:" + param)

                stringText = get_text(param)
                stringRst = check_is_wrong()
                if stringRst == "":
                    __logger.info(str((le+1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != "":
            iresult.status = 1
            __logger.info(u"Interface returns error information:" + str(stringRst))

        iresult.obj = stringText
        iresult.err = stringRst
        iresult.echo_result()
        return iresult
    except Exception as e:
        print(e)
    finally:
        __logger.echo_msg(u"end execute[getText]")


def getHtml(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[getHtml]")

    iresult = IResult()  # new一个返回结果的新对象
    iresult.status = 0  # status初始赋值   status =0 成功  1 表示失败

    try:
        stringText = get_html(param) #取得getHtml方法返回值
        stringRst = check_is_wrong() #判断getHtml方法是否成功

        if stringRst != "":#表示报错了

            for le in range(0,__try_times):
                __logger.info(str((le+1))+"times,"+"Afferent parameter:" + param)

                stringText = get_html(param)
                stringRst = check_is_wrong()
                if stringRst == "":
                    __logger.info(str((le+1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != "":
            iresult.status = 1
            __logger.info(u"Interface returns error information:" + str(stringRst))

        iresult.obj = stringText
        iresult.err = stringRst
        iresult.echo_result()
        return iresult
    except Exception as e:
        print(e)
    finally:
        __logger.echo_msg(u"end execute[getHtml]")

# 返回bool 用于input标签
def existsText(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[existsText]")

    iresult = IResult()
    iresult.status = 0

    try:
        stringText = dll.existsText(param)
        stringRst = check_is_wrong()

        if stringRst != "":

            for le in range(0,__try_times):

                __logger.info(str((le+1))+"times,"+"Afferent parameter:" + param)

                stringText = dll.existsText(param)
                stringRst = check_is_wrong()
                if stringRst == "":
                    __logger.info(str((le+1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != "":
            iresult.status = 1
            __logger.info(u"Interface returns error information:" + str(stringRst))
            
        if stringText == 1:
            iresult.obj = True
        if stringText == 0:
            iresult.obj = False
        iresult.err = stringRst
        iresult.echo_result()
        return iresult
    except Exception as e:
        print(e)
    finally:
        __logger.echo_msg(u"end execute[existsText]")



# # 返回bool  用于input标签
def setText(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[setText]")

    iresult = IResult()
    iresult.status = 0

    try:
        stringText = dll.setText(param)
        stringRst = check_is_wrong()

        if stringRst != "":

            for le in range(0, __try_times):

                __logger.info(str((le+1)) + "times," + "Afferent parameter:" + param)

                stringText = dll.setText(param)
                stringRst = check_is_wrong()
                if stringRst == "":
                    __logger.info(str((le+1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != "":
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))  #自定义异常

        iresult.obj = stringText
        iresult.err = stringRst
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[setText]")


# #返回int  用于select标签  获取页面中select标签中已选中的值
def getVal(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[getVal]")

    iresult = IResult()
    iresult.status = 0

    try:
        stringText = dll.getVal(param)
        stringRst = check_is_wrong()

        if stringRst != "":

            for le in range(0, __try_times):

                __logger.info(str((le+1)) + "times," + "Afferent parameter:" + param)

                stringText = dll.getVal(param)
                stringRst = check_is_wrong()
                if stringRst == "":
                    __logger.info(str((le+1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != "":
            iresult.status = 1
            __logger.info(u"Interface returns error information:" + str(stringRst))

        iresult.obj = stringText
        iresult.err = stringRst
        iresult.echo_result()
        return iresult
    except Exception as e:
        print(e)
    finally:
        __logger.echo_msg(u"end execute[getVal]")



# # 返回bool 用于select标签
# #param='{"activite":"existsVal","input":{"text":"4"},"target":{"selector":"#field1","tag":"SELECT","title":"组织视图首页::部门结构 - 禅道"}}'
# #这边text:4 表示页面上选择的内容是不是第5个，如果是第五个就是返回1，其余返回0，把页面打开，选择第5个标签，然后运行
def existsVal(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[existsVal]")

    iresult = IResult()
    iresult.status = 0

    try:
        stringText = dll.existsVal(param)
        stringRst = check_is_wrong()

        if stringRst != "":

            for le in range(0, __try_times):

                __logger.info(str((le+1)) + "times," + "Afferent parameter:" + param)

                stringText = dll.existsVal(param)
                stringRst = check_is_wrong()
                if stringRst == "":
                    __logger.info(str((le+1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != "":
            iresult.status = 1
            __logger.info(u"Interface returns error information:" + str(stringRst))

        if stringText == 1:
            iresult.obj = True
        if stringText == 0:
            iresult.obj = False
        iresult.err = stringRst
        iresult.echo_result()
        return iresult
    except Exception as e:
        print(e)
    finally:
        __logger.echo_msg(u"end execute[existsVal]")



# # 返回bool 用于checkBox判断是否选中
def doCheck(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[doCheck]")

    iresult = IResult()
    iresult.status = 0

    try:
        stringText = dll.doCheck(param)
        stringRst = check_is_wrong()

        if stringRst != "":

            for le in range(0, __try_times):

                __logger.info(str((le+1)) + "times," + "Afferent parameter:" + param)

                stringText = dll.doCheck(param)
                stringRst = check_is_wrong()
                if stringRst == "":
                    __logger.info(str((le+1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != "":
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = stringText
        iresult.err = stringRst
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[doCheck]")


# # 返回bool
def doRadio(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[doRadio]")

    iresult = IResult()
    iresult.status = 0

    try:
        stringText = dll.doRadio(param)
        stringRst = check_is_wrong()

        if stringRst != "":

            for le in range(0, __try_times):

                __logger.info(str((le+1)) + "times," + "Afferent parameter:" + param)

                stringText = dll.doRadio(param)
                stringRst = check_is_wrong()
                if stringRst == "":
                    __logger.info(str((le+1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != "":
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = stringText
        iresult.err = stringRst
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[doRadio]")


def doClick(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[doClick]")

    iresult = IResult()
    iresult.status = 0

    try:
        stringText = dll.doClick(param)
        stringRst = check_is_wrong()

        if stringRst != "":

            for le in range(0, __try_times):

                __logger.info(str((le+1)) + "times," + "Afferent parameter:" + param)

                stringText = dll.doClick(param)
                stringRst = check_is_wrong()
                if stringRst == "":
                    __logger.info(str((le+1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != "":
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = stringText
        iresult.err = stringRst
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[doClick]")


# # 返回bool
def doDoubleClick(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[doDoubleClick]")

    iresult = IResult()
    iresult.status = 0

    try:
        stringText = dll.doDoubleClick(param)
        stringRst = check_is_wrong()

        if stringRst != "":

            for le in range(0, __try_times):

                __logger.info(str((le+1)) + "times," + "Afferent parameter:" + param)

                stringText = dll.doDoubleClick(param)
                stringRst = check_is_wrong()
                if stringRst == "":
                    __logger.info(str((le+1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != "":
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = stringText
        iresult.err = stringRst
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[doDoubleClick]")


# # 返回bool
def doMouseClick(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[doMouseClick]")

    iresult = IResult()
    iresult.status = 0

    try:
        stringText = dll.doMouseClick(param)
        stringRst = check_is_wrong()

        if stringRst != "":

            for le in range(0, __try_times):

                __logger.info(str((le+1)) + "times," + "Afferent parameter:" + param)

                stringText = dll.doMouseClick(param)
                stringRst = check_is_wrong()
                if stringRst == "":
                    __logger.info(str((le+1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != "":
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = stringText
        iresult.err = stringRst
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[doMouseClick]")


# # 返回bool
def doKeypress(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[doKeypress]")

    iresult = IResult()
    iresult.status = 0

    try:
        stringText = dll.doKeypress(param)
        stringRst = check_is_wrong()

        if stringRst != "":

            for le in range(0, __try_times):

                __logger.info(str((le+1)) + "times," + "Afferent parameter:" + param)

                stringText = dll.doKeypress(param)
                stringRst = check_is_wrong()
                if stringRst == "":
                    __logger.info(str((le+1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != "":
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = stringText
        iresult.err = stringRst
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[doKeypress]")


# # 返回  在lpParamsJson里面设置参数，然后在页面运行，select标签就会选择上与你参数里面对应的值
def doSelect(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[doSelect]")

    iresult = IResult()
    iresult.status = 0

    try:
        stringText = dll.doSelect(param)
        stringRst = check_is_wrong()

        if stringRst != "":

            for le in range(0, __try_times):

                __logger.info(str((le+1)) + "times," + "Afferent parameter:" + param)

                stringText = dll.doSelect(param)
                stringRst = check_is_wrong()
                if stringRst == "":
                    __logger.info(str((le+1)) + "times,try success")
                    break

                time.sleep(1)

        if stringRst != "":
            __logger.info(u"Interface returns error information:" + str(stringRst))
            raise Exception(u"Interface returns error information:" + str(stringRst))

        iresult.obj = stringText
        iresult.err = stringRst
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[doSelect]")


def fun_getpar_web(result, vname1):
    getText = result["return"]
    return getText

def fun_setpar_web(param,text,vname1):

    dic = {}
    paramJason = json.loads(param)
    dic[text] = vname1
    paramJason["input"] = dic
    return json.dumps(paramJason,ensure_ascii=False)

def check_is_wrong():
    erroString = dll.getLastError()

    return string_at(erroString, -1).decode('utf-8')


def get_text(param):
    getText = dll.getText(param)

    return string_at(getText, -1).decode('utf-8')

	
def get_html(param):
    getHtml = dll.getHtml(param)

    return string_at(getHtml, -1).decode('utf-8')












