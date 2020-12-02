# -*- coding: utf-8 -*-
import smtplib
import poplib
import imaplib
import email
import tempfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr
from ubpa.ilog import ILog
import ubpa.encrypt as encrypt
from ubpa.iconstant import *
from ubpa.iresult import MailMessage

__logger = ILog(__file__)
__attachment_path = tempfile.gettempdir()+os.sep  #默认保存路径


def send_smtp_mail(server=None,port=25,psw=None,sender=None,receivers=None,cc=None,bcc=None,subject=None,body=None,attachments=None,ssl='no'):
    '''
SMTP发送邮件
    server:smtp服务器  port:端口号   psw:登陆密码  sender:发送方  receivers:接收者
    cc:抄送  bcc:密抄  subject:标题  body:邮件正文  attachments:附件路径

'''
    __logger.debug('smtp Send mail:[' + str(server) + '][' + str(port) + ']')
    re = []
    try:
        msgRoot = MIMEMultipart()
        #msgRoot['Subject'] = subject   构造标题
        msgRoot['Subject'] = Header(subject, 'utf-8').encode()
        msgRoot['Cc'] = "".join(str(cc))
        msgRoot['Bcc'] = "".join(str(bcc))
        msgRoot['From'] = formataddr(["", sender])
        msgRoot['To'] = formataddr(["", receivers])
        msgRoot.attach(MIMEText(body, 'plain', 'utf-8'))

        if attachments != None:
            for attachment in attachments.split(','):
                rst= os.path.exists(attachment)
                if rst :
                        excelFile = open(attachment, 'rb').read()
                        fileName = os.path.basename(os.path.realpath(attachment))
                        att = MIMEApplication(excelFile)
                        att.add_header('Content-Disposition', 'attachment', fileName=('gbk', '', fileName))
                        msgRoot.attach(att)
                else:
                    __logger.debug(u'Attachment path does not exist')


        if receivers != None and receivers != '':
            re = receivers.split(',')
        if cc != None and cc != '':
            re = re + str(cc).split(',')
        if bcc !=None and bcc != '':
            re = re + str(bcc).split(',')

        smtp = smtplib.SMTP()
        if ssl=='yes':
            smtp = smtplib.SMTP_SSL()
        smtp.connect(server,port)
        psw = encrypt.decrypt(psw)
        smtp.login(sender, psw)
        smtp.sendmail(sender,re, msgRoot.as_string())
        smtp.quit() 
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[sendMail]")



       
def recv_imap_mail(server=None,port=None,psw=None,ssl=False,mail_account=None,mail_inbox='INBOX',attachment_path=None,sender_filter=None,subject_filter=None,body_filter=None,
                 attachments_filter=None,only_unread=True,mark_as_read=True,topn=5):
    '''
    imap收取邮件
        mail_account        :邮箱帐号，为None的时候为默认邮箱
        mail_inbox          :收件箱名称，'收件箱' 或者  'Inbox' ，mail_account为None的时候无效
        sender_filter       :发送邮箱过滤
        subject_filter      :主题过滤
        body_filter         :内容过滤
        attachments_filter  :附件过滤
        only_unread         :只收取未读状态
        mark_as_read        :变为已读状态
        attachment_path     :附件保存路径，默认为当前用户的temp目录
        topn                :收取前n封
    
    Retrun: MailMessage[] 
    '''
    __logger.debug('IMAP receive mail:[' + str(server) + '][' + str(port) + ']')
    mails = []
    try:
        if ssl == True:
            imapServer = imaplib.IMAP4_SSL(server, port)
        else:
            imapServer = imaplib.IMAP4(server, port)
        imapServer.login(mail_account, psw)
        imapServer.select(mail_inbox,readonly = False)
        if only_unread==True:
            resp, items = imapServer.search(None,'Unseen' )
        else:
            resp, items = imapServer.search(None,'All')

        items_mail = items[0].split()
        items_mail = items_mail[0:topn]
        for i in range(len(items_mail)):
            atts = []
            ccs  = []
            file_count = 0
            resp, mailData = imapServer.fetch(items_mail[i], "(RFC822)")
            msg = email.message_from_string(mailData[0][1].decode('utf-8'))
            ls = msg["From"].split(' ')
            if (len(ls) == 2):
                fromname = email.header.decode_header((ls[0]).strip('\"'))
                strfrom = my_unicode(fromname[0][0], fromname[0][1]) + ls[1]
                CC = msg["Cc"]
            else:
                strfrom = msg["From"]
                CC = msg["Cc"]
            mail_from = str(strfrom).split('<')[1].replace('>', '')
            if CC != None:
                cc_list = str(CC).replace(' ','').split(',')
                for cc_info in cc_list:
                    cc_spt =cc_info .split('<')
                    main_cc = email.header.decode_header(cc_spt[0].strip('"'))
                    cc = my_unicode(main_cc[0][0], main_cc[0][1]) + '<'+cc_spt[1]
                    ccs.append(cc)

            subject = email.header.decode_header(msg["Subject"])
            sub = my_unicode(subject[0][0], subject[0][1])
            strdate = msg["Date"]
            attachment_list,filedata_list, mailContent_str = parseEmail(msg)

            if sender_filter != None and not sender_filter in strfrom:
                __logger.debug("filter sender:[" + sender_filter + "]")
                continue
            if subject_filter != None and not subject_filter in sub:
                __logger.debug("filter topic:[" + subject_filter + "]")
                continue
            if body_filter != None and not body_filter in mailContent_str:
                __logger.debug("filter content:[" + body_filter + "]")
                continue
            if attachments_filter != None and len(attachment_list) > 0:
                for i in len(attachment_list):
                    if attachments_filter != None and attachments_filter in attachment_list[i]:
                        if attachment_path == None:
                            attachment_path = __attachment_path
                        savefile(attachment_list[i], filedata_list[i], attachment_path)
                        atts.append(attachment_list[i])
                        file_count = file_count + 1
                    else:
                        __logger.debug("Filter attachments [" + attachments_filter + "]")
                if file_count == 0:
                    continue
            if attachments_filter != None and len(attachment_list) == 0:
                continue

            mail_message = MailMessage()
            mail_message.sender_mail = strfrom
            mail_message.received_time = strdate
            mail_message.subject = sub
            mail_message.body = mailContent_str
            mail_message.cc = ccs
            mail_message.attachments = atts
            mails.append(mail_message)
            if mark_as_read==True:
                imapServer.store(items_mail[i], '+FLAGS', '\\seen')
        imapServer.close()
        imapServer.logout()
        return mails
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[recv_imap_mail]")


def parseEmail(msg):
    '''
    解析邮件方法（区分出正文与附件）
            msg             : 邮件message对象

    Return: (attachment_list,filedata_list,mailContent_str)
    '''
    attachment_list=[]
    filedata_list=[]
    try:
        for part in msg.walk():
            if not part.is_multipart():
                contenttype = part.get_content_type()
                filename = part.get_filename()
                charset = part.get_content_charset()

                if filename:
                    h = email.header.Header(filename)
                    dh = email.header.decode_header(str(h))
                    fname = dh[0][0]
                    encodeStr = dh[0][1]
                    if encodeStr != None:
                        if charset == None:
                            fname = fname.decode(encodeStr)
                        else:
                            fname = fname.decode(charset)
                    data = part.get_payload(decode = True)
                    filedata_list.append(data)
                    attachment_list.append(fname)
                else:
                    if contenttype in ['text/plain']:
                        if charset == None:
                            mailContent = part.get_payload(decode=True)
                            mailContent_str = mailContent.decode()
                        else:
                            mailContent = part.get_payload(decode=True)
                            mailContent_str = mailContent.decode(charset)
                    if contenttype in ['text/html']:
                        continue
        return (attachment_list,filedata_list,mailContent_str)
    except Exception as e:
        raise e


def my_unicode(s, encoding):
    '''
    字符编码转换方法
            s         : 字符串
            encoding  : 编码方式

    return : 编码后的字符串
    '''
    try:
        if encoding :
            s=s.decode(encoding)
            return s
        else:
            return s
    except Exception as e:
        raise e


def savefile(filename, data, path):
    '''
    保存文件方法（保存在指定的根目录下）
            filename: 文件名
            data    : 保存的数据
            path    : 保存路径
    return: 无
    '''
    try:
        filepath = path + filename
        f = open(filepath, 'wb')
        f.write(data)
        f.close()
    except Exception as e:
        __logger.debug("File save failed！")
        raise e





