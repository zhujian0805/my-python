'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class AlipaySystemOauthTokenRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.code = None
		self.grant_type = None
		self.refresh_token = None

	def getapiname(self):
		return 'alipay.system.oauth.token'