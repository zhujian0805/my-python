'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi


class IncrementSubscriptionDeleteRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.subscribe_key = None
        self.subscribe_values = None
        self.topic = None
        self.track_iids = None

    def getapiname(self):
        return 'taobao.increment.subscription.delete'
