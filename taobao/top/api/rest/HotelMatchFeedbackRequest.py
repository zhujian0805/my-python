'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class HotelMatchFeedbackRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.haid = None
		self.hid = None
		self.match_result = None

	def getapiname(self):
		return 'taobao.hotel.match.feedback'