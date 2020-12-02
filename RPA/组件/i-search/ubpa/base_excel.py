import json
import xlwings as xw
import datetime
from ubpa.ilog import ILog
from ubpa.iresult import IResult
import traceback

__logger = ILog(__file__)

def readCell(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[readCell]")

    try:
        iresult = IResult()

        excelPath = json.loads(param)["target"]["excelPath"]
        sheetName = json.loads(param)["target"]["sheet"]
        data = json.loads(param)["target"]["cell"].upper()

        app = xw.App(visible=False, add_book=False)
        wb = app.books.open(excelPath)
        sht = wb.sheets[sheetName]
        cellValue = sht.range(data).value
        iresult.obj = cellValue
        wb.save()
        wb.close()

        iresult.echo_result()
        return iresult
    except Exception as e:
        print(e)
    finally:
        __logger.echo_msg(u"end execute[readCell]")



def writeCell(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[writeCell]")

    try:
        excelPath = json.loads(param)["target"]["excelPath"]
        sheetName = json.loads(param)["target"]["sheet"]
        data = json.loads(param)["target"]["cell"]
        content = json.loads(param)["input"]["text"]

        app = xw.App(visible=False,add_book=False)
        wb = app.books.open(excelPath)
        sht = wb.sheets[sheetName]
        sht.range(data).options(index=False).value = content
        wb.save()
        wb.close()
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[writeCell]")




