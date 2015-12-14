#!/usr/bin/python
import math

class Circle(object):
  def __init__(self,radius):
    self.radius = radius
    # Some additional properties of Circles
  @property
  def area(self):
    return math.pi*self.radius**2

  @property
  def perimeter(self):
    return 2*math.pi*self.radius

c = Circle(4.0)
print c.radius
print c.area
print c.perimeter
