'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class TmallEaiOrderRefundOrderHoldRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.hold_result = None
		self.hold_step = None
		self.hold_time = None
		self.refund_id = None
		self.refund_phase = None

	def getapiname(self):
		return 'tmall.eai.order.refund.order.hold'
