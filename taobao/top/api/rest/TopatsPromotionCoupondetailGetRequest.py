'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class TopatsPromotionCoupondetailGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.coupon_id = None
		self.end_time = None
		self.start_time = None
		self.state = None

	def getapiname(self):
		return 'taobao.topats.promotion.coupondetail.get'
