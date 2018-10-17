'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi


class PromotionmiscItemActivityListGetRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.page_no = None
        self.page_size = None

    def getapiname(self):
        return 'taobao.promotionmisc.item.activity.list.get'
