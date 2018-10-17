'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi


class SimbaAdgroupCatmatchUpdateRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.adgroup_id = None
        self.catmatch_id = None
        self.max_price = None
        self.nick = None
        self.online_status = None
        self.use_default_price = None

    def getapiname(self):
        return 'taobao.simba.adgroup.catmatch.update'
