'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi


class WaimaiItemAddRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.auctiondesc = None
        self.auctionstatus = None
        self.categoryid = None
        self.goodsno = None
        self.limitbuy = None
        self.oriprice = None
        self.picurl = None
        self.price = None
        self.quantity = None
        self.shopids = None
        self.title = None
        self.viceimage = None

    def getapiname(self):
        return 'taobao.waimai.item.add'
