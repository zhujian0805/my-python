'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class EbookmediaChapterUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.auction_id = None
		self.content = None
		self.content_url = None
		self.is_free = None
		self.price_count = None
		self.tbid = None
		self.title = None
		self.word_count = None

	def getapiname(self):
		return 'taobao.ebookmedia.chapter.update'
