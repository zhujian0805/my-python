#!/usr/bin/python
# -*- coding: utf-8 -*-

import mechanize
from BeautifulSoup import BeautifulSoup

import logging
log = logging.getLogger("DropBoxClass")

class DropBoxClass:
    """ Class which handles dropbox operations through it's web interface by using 
    mechanize 

    """

    #different paths defined as static 
    loginPath = "https://www.dropbox.com/login"
    uploadPath = "https://dl-web.dropbox.com/upload"
    accountPath = "https://www.dropbox.com/account"

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

        br['login_email'] = self._username
        br['login_password'] = self._password
        
        #log in
        br.submit()
        
        return br
        
    def uploadFile(self, filename, path="/"):
        """ Upload a file with filename 'filename' to Dropbox 
        If such file do exist already on DropBox it will be overwritten"""

        isUploadForm = lambda u: u.action == self.uploadPath and u.method == "POST"
        
        log.debug("selecting form")
        self._br.select_form(predicate=isUploadForm)
        
        log.debug("finding control")
        self._br.form.find_control("dest").readonly = False

        log.debug("setting value")
        self._br.form.set_value(path,"dest")
        
        try:
            log.debug("opening file")
            f = open(filename)

            log.debug("adding file to form")
            self._br.form.add_file(f, "", filename)

            log.debug("submitting form")
            self._br.submit()
        except IOError, e:
            log.error("IOError occured, e: %s" % (e))
            log.error("File not uploaded")
        
    def _parseUsage(self, s):
        """ returns the used space in MB"""
        
        #find the first occurence of (, indicating the first value
        i1 = s.find("(")
        
        if i1 < 0: 
            log.error("Site structure has changed, cannot find first occurence of '('")
            return None
        
        i1 += 1 #value starts after paranthesis
        i2 = s.find("MB")
        
        if i2 > 0: #meaning it's defined in MB
            return float(s[i1:i2])
        else: #try with GB otherwise
            i2 = s.find("GB")
            if i2 > 0: 
                return float(s[i1:i2])
            else:
                log.error("Site structure changed, storage isn't indicated in either MB or GB")
                return None
    
    def _parseStorageSize(self, s):
        """ returnes the total space in MB"""
        return (float(s[s.find("of")+2:s.find("GB")]))*1000
    
    def getFreeSpace(self):
        """ returns an estimate of  free space on DropBox by calculating from the usage bar from account page
        currently it only handles if the values are presented in MB or GB. 

        Assumption: The bar presents information as: "28,5% used (583.3MB/GB of 2GB)",
        
        returns value in MB.
        """
        self._br.open(self.accountPath)
        soup = BeautifulSoup(self._br.response().read())

        element = soup.find("span", { "id" : "usage-percent" })
        
        if element == None:
            log.error("Site structure has changed, usage percentage span doesn't exist under account page")
            return None
        
        #parse out the string
        s = element.string
        usage = self._parseUsage(s)
        storage = self._parseStorageSize(s)
        if usage != None:
            return storage - usage
        else:
            exit(1)
