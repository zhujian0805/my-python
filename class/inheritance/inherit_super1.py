#!/usr/bin/python
# Filename: inherit.py

class SchoolMember(object):
	'''Represents any school member.'''
	def __init__(self,name,age):
		self.name=name
		self.age=age
		print '(Initialized SchoolMember: %s)' %self.name
	
	def tell(self):
		'''Tell my details.'''
		print 'Name:"%s" Age:"%s"' %(self.name,self.age),

class Teacher(SchoolMember):
	'''Represents a teacher.'''
	def __init__(self,name,age,salary):
		#SchoolMember.__init__(self,name,age)
                super(Teacher, self).__init__(name, age)
		self.salary=salary
		print '(Initialized Teacher: %s)' %self.name
	
	def tell(self):
		#SchoolMember.tell(self)
                super(Teacher, self).tell()
		print 'Salary: "%d"' %self.salary

t=Teacher('Mrs. Shrividya',40,30000)
print # prints a blank line
