'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi


class SimbaAdgroupCampcatmatchsGetRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.campaign_id = None
        self.nick = None
        self.page_no = None
        self.page_size = None

    def getapiname(self):
        return 'taobao.simba.adgroup.campcatmatchs.get'
