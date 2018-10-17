#!/usr/bin/python
# Include the Dropbox SDK libraries
"""This script fully automate the dropbox operation, including the login, OAuth
authentication, and the click allow function which allow no human intervention at allow

this is just a example code
"""
from dropbox import client, rest, session
from pprint import pprint
import mechanize
from BeautifulSoup import BeautifulSoup
import time
import sys
import logging

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def click_allow(username, password, link):

    loginPath = "https://www.dropbox.com/login"
    uploadPath = "https://dl-web.dropbox.com/upload"
    accountPath = "https://www.dropbox.com/account"

    br = mechanize.Browser()
    br.open(loginPath)
    isLoginForm = lambda l: l.action == loginPath and l.method == "POST"
    br.select_form(predicate=isLoginForm)
    br['login_email'] = username
    br['login_password'] = password
    logger.info("click %s" % loginPath)
    br.submit()
    logger.info("click %s" % link)
    br.open(link)
    br.select_form(nr=0)
    req = br.click(type='submit', nr=1)
    br.open(req)


class DropboxClass:
    def __init__(self, key, secret, username, password, access_type):
        self.key = key
        self.secret = secret
        self.access_type = access_type
        self.username = username
        self.password = password
        self.sess = None

    def setSession(self):

        self.sess = session.DropboxSession(self.key, self.secret,
                                           self.access_type)
        request_token = self.sess.obtain_request_token()
        url = self.sess.build_authorize_url(request_token)
        logger.info("visit %s to authorize your app" % url)
        click_allow(self.username, self.password, url)

        raw_input()

        access_token = self.sess.obtain_access_token(request_token)
        self.sess.set_token(access_token.key, access_token.secret)

    def getAccInfo(self):
        self.dropbox_client = client.DropboxClient(self.sess)
        try:
            dropbox_info = self.dropbox_client.account_info()
            print dropbox_info
        except:
            print "Failed to get account_info"

    def dlfile(self):
        f, metadata = self.dropbox_client.get_file_and_metadata('testingfile')
        out = open('testingfile', 'wb')
        out.write(f.read())
        out.close()
        print metadata

    def lsfile(self):
        folder_metadata = self.dropbox_client.metadata('/')
        pprint(folder_metadata)


def main(key, secret, username, password, access_type):
    dropb = DropboxClass(key, secret, username, password, access_type)
    dropb.setSession()
    dropb.getAccInfo()
    dropb.dlfile()
    dropb.lsfile()


if __name__ == '__main__':
    logger.info("Starting the script")
    APP_KEY = sys.argv[1]
    APP_SECRET = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    #ACCESS_TYPE = 'app_folder'
    ACCESS_TYPE = 'auto'
    #ACCESS_TYPE = 'dropbox'
    main(APP_KEY, APP_SECRET, username, password, ACCESS_TYPE)
