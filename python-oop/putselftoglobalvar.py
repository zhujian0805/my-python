#!/usr/bin/python

try:
  emp_map
except NameError:
  emp_map = {}

class Employee:
  'Common base class for all employees'
  empCount = 0

  def __init__(self, name, salary):
    self.name = name
    self.salary = salary
    self.map = emp_map
    Employee.empCount += 1
    self.add_emp()
	
  def displayCount(self):
    print "Total Employee %d" % Employee.empCount
	
  def displayEmployee(self):
    print "Name : ", self.name,  ", Salary: ", self.salary
	
  def add_emp(self):
    self.map[self.name] = self

emp1 = Employee("Zara", 2000)
emp2 = Employee("Manni", 5000)

for k in emp_map.keys():
  emp_map[k].displayEmployee()
