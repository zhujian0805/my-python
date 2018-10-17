#!/usr/bin/python
# -*- coding: utf-8 -*-

import mechanize
from BeautifulSoup import BeautifulSoup

import logging
log = logging.getLogger("DropBoxClass")


class JiraClient:
    """ Class which handles dropbox operations through it's web interface by using 
    mechanize 

    """

    #different paths defined as static
    loginPath = "https://jira.sample.net/login.jsp"

    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._br = self.__login()
        log.info("initiating DropBoxClass")

    def __login(self):
        """ returns an initialized mechanize browser 
        which has logged in to DropBox """

        br = mechanize.Browser()
        br.open(self.loginPath)

        isLoginForm = lambda l: l.action == self.loginPath and l.method == "POST"
        br.select_form(predicate=isLoginForm)

        br['os_username'] = self._username
        br['os_password'] = self._password

        #log in
        br.submit()

        return br


if __name__ == '__main__':
    jira = JiraClient('jameszhu', 'Q1w2e3r4')
