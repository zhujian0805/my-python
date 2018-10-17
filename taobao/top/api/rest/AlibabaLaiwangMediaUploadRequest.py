'''
Created by auto_sdk on 2014-03-10 13:11:08
'''
from top.api.base import RestApi


class AlibabaLaiwangMediaUploadRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.media = None
        self.type = None

    def getapiname(self):
        return 'alibaba.laiwang.media.upload'

    def getMultipartParas(self):
        return ['media']
