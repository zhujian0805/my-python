import datetime
cur = datetime.datetime.now()

num = 1
a_list = {"a":1, "b":2, "c":3}
while num < 100000:
    if a_list.has_key("a"):
        pass
    num += 1

now = datetime.datetime.now()
print (now - cur).total_seconds()