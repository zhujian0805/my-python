'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class ScitemMapBatchQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.outer_code = None
		self.page_index = None
		self.page_size = None
		self.sc_item_id = None

	def getapiname(self):
		return 'taobao.scitem.map.batch.query'
