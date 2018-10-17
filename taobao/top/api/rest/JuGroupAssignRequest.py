'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi


class JuGroupAssignRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.fields = None
        self.terminal_type = None
        self.uuid = None

    def getapiname(self):
        return 'taobao.ju.group.assign'
