'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class IncrementAuthorizeMessageGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.end_modified = None
		self.nick = None
		self.page_no = None
		self.page_size = None
		self.start_modified = None
		self.status = None
		self.topic = None

	def getapiname(self):
		return 'taobao.increment.authorize.message.get'