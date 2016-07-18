'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class TaobaokeMobileShopsGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.cid = None
		self.end_auctioncount = None
		self.end_commissionrate = None
		self.end_credit = None
		self.end_totalaction = None
		self.fields = None
		self.keyword = None
		self.only_mall = None
		self.outer_code = None
		self.page_no = None
		self.page_size = None
		self.sort_field = None
		self.sort_type = None
		self.start_auctioncount = None
		self.start_commissionrate = None
		self.start_credit = None
		self.start_totalaction = None

	def getapiname(self):
		return 'taobao.taobaoke.mobile.shops.get'
