import datetime as DT
from matplotlib import pyplot as plt
from matplotlib.dates import date2num

data = [
    (DT.datetime.strptime('2010-02-05 01:01:01', "%Y-%m-%d %H:%M:%S"), 123),
    (DT.datetime.strptime('2010-02-19 02:02:02', "%Y-%m-%d %H:%M:%S"), 678),
    (DT.datetime.strptime('2010-03-05 02:02:03', "%Y-%m-%d %H:%M:%S"), 987),
    (DT.datetime.strptime('2010-03-19 02:01:01', "%Y-%m-%d %H:%M:%S"), 345)
]

x = [date2num(date) for (date, value) in data]
y = [value for (date, value) in data]

fig = plt.figure()

graph = fig.add_subplot(111)

# Plot the data as a red line with round markers
graph.plot(x, y, 'r-o')

# Set the xtick locations to correspond to just the dates you entered.
graph.set_xticks(x)

# Set the xtick labels to correspond to just the dates you entered.
graph.set_xticklabels(
    [date.strftime("%Y-%m-%d %H:%M:%S") for (date, value) in data])

plt.show()
