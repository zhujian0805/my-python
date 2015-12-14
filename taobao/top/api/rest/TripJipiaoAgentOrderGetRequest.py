'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class TripJipiaoAgentOrderGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.order_ids = None

	def getapiname(self):
		return 'taobao.trip.jipiao.agent.order.get'
