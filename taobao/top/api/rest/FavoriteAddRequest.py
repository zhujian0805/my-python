'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class FavoriteAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.collect_type = None
		self.item_numid = None
		self.shared = None

	def getapiname(self):
		return 'taobao.favorite.add'
