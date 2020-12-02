# -*- coding: utf-8 -*-
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from ctypes import *
import datetime
import traceback

from ubpa.ilog import ILog
from ubpa.iresult import IResult

__logger = ILog(__file__)

def sendMail(param):
    __logger.info(u"Afferent parameter:" + param)
    __logger.echo_msg(u"Ready to execute[sendMail]")

    try:
        iresult = IResult()

        msgRoot = MIMEMultipart()
        target = json.loads(param)["target"]
        host = target.get('host', "")
        port = target.get('port', "")
        username = target.get('username', "")
        password = target.get('password', "")
        sender = target.get('sender', "")
        receiver = target.get('receiver', "")
        cc = target.get('cc', "")

        input = json.loads(param)["input"]
        subject = input.get('subject', "")
        body = input.get('body', "")
        fileDir = input.get('fileDir', "")

        if len(fileDir) > 0:
            fileDirs = fileDir.split(",")
            for s in fileDirs:
                excelFile = open(s, 'rb').read() #单个附件
                if s.find("/")>=0:
                    file = s.split("/")
                else:
                    file = s.split("\\")
                fileName = file[len(file)-1]
                att = MIMEApplication(excelFile)
                att.add_header('Content-Disposition', 'attachment', filename=('gb2312', '',fileName))
                msgRoot.attach(att)  # 构造附件

        bodyText = MIMEText(body)

        msgRoot['Subject'] = subject #构造标题
        msgRoot.attach(bodyText) #构造正文
        msgRoot['Cc'] = cc #构造抄送
        msgRoot['From'] = sender
        msgRoot['To'] = receiver

        if cc != "":
            re = receiver.split(',') + cc.split(',')
        else:
            re = receiver.split(',')

        smtp = smtplib.SMTP()
        smtp.connect(host,port)
        smtp.login(username, password)
        smtp.sendmail(sender,re,msgRoot.as_string())
        smtp.quit()

        iresult.status = 0
        iresult.echo_result()
        return iresult
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[sendMail]")


