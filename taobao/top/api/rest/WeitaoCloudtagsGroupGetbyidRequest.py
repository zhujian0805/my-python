'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi


class WeitaoCloudtagsGroupGetbyidRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.group_id = None

    def getapiname(self):
        return 'taobao.weitao.cloudtags.group.getbyid'
