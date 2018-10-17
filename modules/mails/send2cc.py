#!/usr/bin/python

import smtplib
from email.mime.text import MIMEText

mail_host = 'connect-cn.james.com'
mail_user = 'svcCNGameCCUreport@james.com'
mail_pwd = 'XXXXXXXXXX'
mail_to = 'jzhu@james.com,jzhu1@company.com'
mail_cc = 'jzhu@james.com, jzhu2@company.com'
mail_bcc = 'jzhu@james.com'
content = 'this is a mail sent with python'

msg = MIMEText(content)
msg['From'] = mail_user
msg['Subject'] = 'this is a python test mail'
msg['To'] = mail_to
msg['Cc'] = mail_cc
msg['Bcc'] = mail_bcc
try:
    s = smtplib.SMTP()
    s.set_debuglevel(1)
    s.connect(mail_host)
    s.starttls()
    s.login(mail_user, mail_pwd)

    s.sendmail(mail_user, [mail_to, mail_cc, mail_bcc], msg.as_string())
    s.close()
    print 'success'
except Exception, e:
    print e
