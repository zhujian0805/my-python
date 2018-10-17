'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi


class HotelOrderFaceDealRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.oid = None
        self.oper_type = None
        self.reason_text = None
        self.reason_type = None

    def getapiname(self):
        return 'taobao.hotel.order.face.deal'
