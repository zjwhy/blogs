# -*- coding:utf-8 -*-
from _operator import length_hint
from builtins import str
from datetime import datetime
import os
import tempfile

import win32com.client

from ubpa.iresult import MailMessage
from ubpa.ilog import ILog   
from ubpa.iresult import IResult
import win32com.client as win32 


__logger = ILog(__file__) 
__attachment_path = tempfile.gettempdir()+os.sep  #默认保存路径


'''
发送邮件:
      mailMsg = MailMessage()
#     mailMsg.to='13813828052@163.com;wux@i-search.com.cn'
#     mailMsg.cc = '13813828052@163.com;84870911@qq.com'
#     mailMsg.subject='test subject'
#     mailMsg.body='test body'
#     atts = []
#     atts.append('e:/1.gif')
#     atts.append('e:/11.gif')
#     mailMsg.attachments=atts
#     iresult = send_outlook(mailMsg)
'''
def send_outlook(receiver = None,cc = None, bcc = None, subject = None, body = None, attachments = None):
    __logger.echo_msg(u"Ready to execute[send_outlook]")
    iresult = IResult()

    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail=outlook.CreateItem(0)

        if receiver != None:
            tos_receiver = receiver.split(";")
            for to in tos_receiver:
                mail.Recipients.Add(to)
        if cc != None:
            mail.CC = cc
        if bcc != None:
            mail.BCC = bcc
        if subject != None:
            mail.Subject = subject
        if body!= None:
            mail.Body = body
        if attachments!=None:
            attachment_list = attachments.split(",")
            for att in attachment_list:
                mail.Attachments.Add(att,1,1,'我的文件')

        mail.Send() 
        iresult.obj=True
    except BaseException as ex: 
        iresult.status = 1
        iresult.err = u"Program execution error"+str(ex)
        __logger.error(u"Program execution error"+str(ex)) 
        iresult.obj=False                
    finally:
        __logger.echo_msg(u"end execute[send_outlook]") 
        iresult.echo_result()
        return iresult   
    

'''
获取Outlook收件箱
    mail_account:邮箱帐号
    mail_inbox  :收件箱名称，'收件箱' 或者  'Inbox' ，mail_account为None的时候无效
'''
def get_inbox(mail_account=None,mail_inbox='收件箱'):
    inbox = None

    try:
        outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
        if mail_account==None :
            inbox = outlook.GetDefaultFolder(6) 
        else:
            for i in range(10):
                try:
                    mail_box = outlook.Folders.Item(i)
                    mb_name = mail_box.Name
                    if mail_account in mb_name:
                        for j in range(100):
                            try:
                                inbox = mail_box.Folders[j]
                                ib_name = inbox.Name
                                if mail_inbox in ib_name :
                                    break
                            except:
                                pass 
                        break                       
                except:
                    pass  
    finally: 
        return inbox
       
'''
收取Outlook 邮件
    mail_account        :邮箱帐号
    mail_inbox          :收件箱名称，'收件箱' 或者  'Inbox' ，mail_account为None的时候无效
    sender_filter       :发送邮箱过滤
    subject_filter      :主题过滤
    body_filter         :内容过滤
    attachments_filter  :附件过滤
    only_unread         :只收取未读状态
    mark_as_read        :变为已读状态
    attachment_path     :附件保存路径，默认为当前用户的temp目录
    top                 :收取前n条

Retrun: MailMessage[] 
'''
def recv_outlook(mail_account=None, mail_inbox='收件箱', sender_filter=None, subject_filter=None, body_filter=None,
                 attachments_filter=None, only_unread=True, mark_as_read=False, attachment_path=None, top=None):
    __logger.echo_msg(u"Ready to execute[outlook_recv]")
    mails = []
    n = 1

    try:
        inbox = get_inbox(mail_account, mail_inbox)
        if inbox != None:
            messages = inbox.Items

            if only_unread:
                messages = messages.Restrict('[UnRead] = True')  # 未读取的邮件

            messages.Sort("[ReceivedTime]", True)  # 收件时间倒序

            if top == None:
                top = len(messages)

            __logger.debug(u"total receive[" + str(len(messages)) + "]copies of mails,get Topn:" + str(top))

            for message in messages:
                atts = []
                flag = False

                if n > top:
                    break

                sender = message.SenderEmailAddress
                subject = message.Subject
                body = message.Body
                cc = message.CC
                received_time = str(message.ReceivedTime)
                attachments = message.Attachments

                if sender_filter != None and not sender_filter in sender:
                    continue
                else:
                    flag = True

                if subject_filter != None and not subject_filter in subject:
                    continue
                else:
                    flag = True

                if body_filter != None and not body_filter in body:
                    continue
                else:
                    flag = True

                if attachments_filter != None and len(attachments) > 0:
                    for attachment in attachments:
                        file_name = attachment.FileName
                        k = 0

                        if attachments_filter != None and attachments_filter in file_name:

                            flag = True
                            if attachment_path == None:
                                attachment_path = __attachment_path

                            att_file_path = attachment_path + os.sep + file_name
                            attachment.SaveAsFile(att_file_path)
                            atts.append(att_file_path)
                            k = k + 1
                        else:
                            if k == 0:
                                flag = False

                if attachments_filter != None and len(attachments) == 0:
                    continue

                if attachments_filter == None and len(attachments) > 0:
                    for attachment in attachments:
                        file_name = attachment.FileName
                        if attachment_path == None:
                            attachment_path = __attachment_path

                        att_file_path = attachment_path + os.sep + file_name
                        attachment.SaveAsFile(att_file_path)
                        atts.append(att_file_path)

                if flag == True:
                    mail_message = MailMessage()
                    mail_message.sender_mail = sender
                    mail_message.received_time = received_time
                    mail_message.subject = subject
                    mail_message.body = body
                    mail_message.cc = cc
                    mail_message.attachments = atts

                    mails.append(mail_message)

                    n = n + 1
                    if mark_as_read:
                        message.UnRead = False  # 标志为已读

    except BaseException as ex:
        __logger.error(u"Program execution error")

    finally:
        __logger.echo_msg(u"end execute[outlook_recv]")

        return mails
    
