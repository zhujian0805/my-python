'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class TaobaokeItemsConvertRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.is_mobile = None
		self.nick = None
		self.num_iids = None
		self.outer_code = None
		self.pid = None
		self.refer_type = None
		self.track_iids = None

	def getapiname(self):
		return 'taobao.taobaoke.items.convert'
