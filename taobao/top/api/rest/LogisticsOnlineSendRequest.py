'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class LogisticsOnlineSendRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.cancel_id = None
		self.company_code = None
		self.feature = None
		self.is_split = None
		self.out_sid = None
		self.seller_ip = None
		self.sender_id = None
		self.sub_tid = None
		self.tid = None

	def getapiname(self):
		return 'taobao.logistics.online.send'