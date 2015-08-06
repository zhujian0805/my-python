'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class SimbaAdgroupOnlineitemsvonGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.nick = None
		self.order_by = None
		self.order_field = None
		self.page_no = None
		self.page_size = None

	def getapiname(self):
		return 'taobao.simba.adgroup.onlineitemsvon.get'
