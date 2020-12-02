from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from ._core import visual_action
import os
import smtplib
from datetime import datetime

@visual_action
def send_email(**args):
    sender = args['sender']
    sender_display_name = args['sender_display_name']
    to = args['to']
    cc = args['cc']
    bcc = args['bcc']
    subject = args['subject']
    body = args['body']
    body_is_html = args['body_is_html']
    attachments = args['attachments']

    select_smtp_server = args['select_smtp_server']
    use_ssl = args['use_ssl']

    smtp_server = None
    smtp_port = None

    if select_smtp_server == 'qq_smtp':
        use_ssl = True
        smtp_server = 'smtp.qq.com'
        smtp_port = '465'
    elif select_smtp_server == '126_smtp':
        smtp_server = 'smtp.126.com'
        smtp_port = '465' if use_ssl else '25'
    elif select_smtp_server == '163_smtp':
        smtp_server = 'smtp.163.com'
        smtp_port = '465' if use_ssl else '25'
    else:
        smtp_server = args['smtp_server']
        smtp_port = args['smtp_port']

    smtp_server_authentication = args['smtp_server_authentication']
    user_name = args['user_name']
    password = args['password']
     
    # 邮件
    msg = MIMEMultipart()

    # 邮件正文
    content = MIMEText(
        body, 
        'html' if body_is_html else 'plain', 
        'utf-8')
    msg.attach(content)

    if sender_display_name:
        msg['From'] = sender_display_name + '<' + sender + '>'
    else:
        msg['From'] = sender

    msg['To'] = to
    msg['Cc'] = cc
    msg['Bcc'] = bcc
    msg['Subject'] = Header(subject, 'utf-8')
    # 可能是因为mailkit的问题导致邮件触发器收不到邮件，所以需要手动地添加一下邮件的发送时间
    msg['Date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 邮件附件
    if attachments:
        file_paths = attachments.split(';')
        for file_path in file_paths:
            file_path = file_path.strip()
            if len(file_path) != 0:
                file = MIMEApplication(open(file_path, 'rb').read())
                file.add_header('Content-Disposition', 'attachment', filename = os.path.basename(file_path))
                msg.attach(file)

    # SMTP 服务器
    server = None
    if use_ssl:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    else:
        server = smtplib.SMTP(smtp_server, smtp_port)

    if smtp_server_authentication:
        try:
            server.starttls()
        except:
            pass
        server.login(user_name, password)

    all_to = ''
    if to:
        all_to += (to + ';')
    if cc:
        all_to += (cc + ';')
    if bcc:
        all_to += (bcc + ';')
    all_to = all_to.split(';')
    while '' in all_to:
        all_to.remove('')
    server.sendmail(sender, all_to, msg.as_string())
    server.quit()