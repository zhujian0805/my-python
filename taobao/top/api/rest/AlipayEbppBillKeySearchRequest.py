'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class AlipayEbppBillKeySearchRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.charge_inst = None
		self.end_time = None
		self.fields = None
		self.only_subscribed = None
		self.order_type = None
		self.start_time = None
		self.sub_order_type = None

	def getapiname(self):
		return 'alipay.ebpp.bill.key.search'
