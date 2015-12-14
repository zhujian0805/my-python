'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class FenxiaoCooperationProductcatAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.cooperate_id = None
		self.grade_id = None
		self.product_line_list = None

	def getapiname(self):
		return 'taobao.fenxiao.cooperation.productcat.add'
