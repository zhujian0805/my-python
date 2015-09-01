#!/usr/bin/python

import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import time

n=20
duration=1000
now=time.mktime(time.localtime())
timestamps=np.linspace(now,now+duration,n)
dates=[dt.datetime.fromtimestamp(ts) for ts in timestamps]
datenums=md.date2num(dates)
values=np.sin((timestamps-now)/duration*2*np.pi)
values1=np.sin((timestamps-now)/duration*3*np.pi)
values2=np.log((timestamps-now)/duration*2*np.pi)
plt.subplots_adjust(bottom=0.2)
plt.xticks( rotation=25 )
ax=plt.gca()
xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
plt.plot(datenums,values)
plt.plot(datenums,values1)
plt.plot(datenums,values2)
plt.legend()
plt.show()
