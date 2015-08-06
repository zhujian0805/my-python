'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class TbkShopsConvertRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.nick = None
		self.outer_code = None
		self.pid = None
		self.seller_nicks = None
		self.sids = None

	def getapiname(self):
		return 'taobao.tbk.shops.convert'
