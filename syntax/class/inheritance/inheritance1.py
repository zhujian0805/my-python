#!/usr/bin/python

from pprint import pprint


class ContactList(list):
    def search(self, name):
        '''return all contacts that contain the search valeu in their name'''
        matching_contacts = []
        for contact in self:
            if name in contact.name:
                matching_contacts.append(contact)
        return matching_contacts


class contact:
    all_contacts = ContactList()

    def __init__(self, name, email, phone=110):
        self.name = name
        self.email = email
        self.phone = phone
        self.all_contacts.append(self)


c1 = contact('James Zhu', 'jameszhu@sample.com')
c1 = contact('Andy Lau', 'aqian@sample.com')

for i in c1.all_contacts.search('a'):
    print i.name, i.email
