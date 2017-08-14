# http://python.jobbole.com/83747/
class Province:
    country = 'China'

    def __init__(self, name, count):
        self.name = name
        self.count = count

    def func(self, *args, **kwargs):
        print 'func'

print Province.__dict__
obj1 = Province('HeBei', 10000)
print obj1.__dict__
obj2 = Province('HeNan', 3888)
print obj2.__dict__
