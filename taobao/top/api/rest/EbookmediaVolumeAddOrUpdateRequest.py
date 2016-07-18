'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class EbookmediaVolumeAddOrUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.auction_id = None
		self.desc = None
		self.order_id = None
		self.title = None

	def getapiname(self):
		return 'taobao.ebookmedia.volume.add.or.update'
