#!/usr/bin/python


def coroutine(func):
    def start(*args, **kwargs):
        g = func(*args, **kwargs)
        g.next()
        return g

    return start


@coroutine
def receiver():
    print("Ready to receive")
    while True:
        n = (yield)
        print("Got %s" % n)
        # Example use


r = receiver()
r.send("Hello World")

r.close()

#r.send("Hello World")
