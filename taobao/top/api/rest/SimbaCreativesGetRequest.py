'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class SimbaCreativesGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.adgroup_id = None
		self.creative_ids = None
		self.nick = None

	def getapiname(self):
		return 'taobao.simba.creatives.get'
