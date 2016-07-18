#!/usr/bin/python


def myclass_init(self, my_attr):
    self.my_attribute = my_attr


MyClass = type("MyClass", (object, ), {"my_attribute": 0,
                                       "__init__": myclass_init})

o = MyClass("Test")
print o.my_attribute
