'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi


class TmallEaiOrderRefundGoodReturnRefuseRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.refund_id = None
        self.refund_phase = None
        self.refund_version = None
        self.refuse_message = None
        self.refuse_proof = None

    def getapiname(self):
        return 'tmall.eai.order.refund.good.return.refuse'

    def getMultipartParas(self):
        return ['refuse_proof']
