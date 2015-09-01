#!/usr/bin/python

from matplotlib import pyplot as plt
from matplotlib import dates
from datetime import datetime
import sys

d = []
t = []
fh = open("data.txt")
for line in fh.readlines():
  dstamp, temp = line.rstrip().split(" ")
  d.append(datetime.strptime(dstamp, '%Y-%m-%d-%H-%M-%S'))
  t.append(int(temp))
fh.close()

mins = dates.MinuteLocator(1)
days = dates.DayLocator()
hours = dates.HourLocator()
dfmt = dates.DateFormatter('%b %d')

datemin = datetime(2015, 1, 4, 0, 0, 0)
datemax = datetime(2015, 1, 4, 23, 59, 59)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_locator(mins)
ax.xaxis.set_major_formatter(dfmt)
ax.xaxis.set_minor_locator(mins)
ax.set_xlim(datemin, datemax)
ax.set_ylabel('Temperature (F)')
ax.grid(True)
ax.plot(d, t, linewidth=2)
fig.set_size_inches(8, 4)

plt.show()
#plt.savefig('temperatures.pdf', format='pdf')
