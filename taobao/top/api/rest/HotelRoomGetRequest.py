'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi
class HotelRoomGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.gid = None
		self.item_id = None
		self.need_hotel = None
		self.need_room_desc = None
		self.need_room_quotas = None
		self.need_room_type = None

	def getapiname(self):
		return 'taobao.hotel.room.get'
