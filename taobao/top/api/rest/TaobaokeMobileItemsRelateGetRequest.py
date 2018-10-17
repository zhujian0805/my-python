'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi


class TaobaokeMobileItemsRelateGetRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.cid = None
        self.fields = None
        self.max_count = None
        self.num_iid = None
        self.outer_code = None
        self.refer_type = None
        self.relate_type = None
        self.seller_id = None
        self.shop_type = None
        self.sort = None
        self.track_iid = None

    def getapiname(self):
        return 'taobao.taobaoke.mobile.items.relate.get'
