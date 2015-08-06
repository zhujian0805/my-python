#!/usr/bin/python

from pprint import pprint

class contact:
  all_contacts = [] 

  def __init__(self, name, email, phone=110):
    self.name = name
    self.email = email
    self.phone = phone
    self.all_contacts.append(self)


c1 = contact('James Zhu', 'jameszhu@sample.com')
c1 = contact('Andy Lau', 'aqian@sample.com')

for i in c1.all_contacts:
  print i.name, i.email
