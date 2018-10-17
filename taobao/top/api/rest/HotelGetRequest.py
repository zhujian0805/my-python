'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi


class HotelGetRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.check_audit = None
        self.hid = None
        self.need_room_type = None

    def getapiname(self):
        return 'taobao.hotel.get'
