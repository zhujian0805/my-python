#!/usr/bin/env python

import smtplib
from email.mime.text import MIMEText

s = smtplib.SMTP('localhost')
s.set_debuglevel(1)
msg = MIMEText("""body""")
sender = 'James Zhu'
recipients = ['28442902@qq.com', 'zhujian0805@gmail.com']
msg['Subject'] = "subject line"
msg['From'] = sender
msg['To'] = ", ".join(recipients)
s.sendmail(msg.get('From'), recipients, msg.as_string())
