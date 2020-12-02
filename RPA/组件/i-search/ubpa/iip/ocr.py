
# -*- coding: utf-8 -*-

"""
图像识别
"""

from .base import IipOcrBase
from .base import base64
from .base import json
from .base import urlencode
from .base import quote

class IipOcr(IipOcrBase):

    """
    图像识别
    """

    '''通用文字识别'''
    __generalBasicUrl = 'http://api.i-search.com.cn/ocr/general_basic'

    '''身份证识别'''
    __idcardUrl = 'http://api.i-search.com.cn/ocr/idCard'

    '''营业执照'''
    __businessLicenseUrl = 'http://api.i-search.com.cn/ocr/businessLicense'

    '''验证码'''
    __vCodeUrl = 'http://api.i-search.com.cn/ocr/vCode'
    
    
    def basicGeneral(self, image, options=None):
        """
            通用文字识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        data.update({"apiKey": self._apiKey, "secretKey": self._secretKey})

        return self._request(self.__generalBasicUrl, data)
     
     
    def idcard(self, image, options=None):
        """
            身份证识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        data.update({"apiKey": self._apiKey, "secretKey": self._secretKey})

        return self._request(self.__idcardUrl, data)
    

    def businessLicense(self, image, options=None):
        """
            营业执照识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        data.update({"apiKey": self._apiKey, "secretKey": self._secretKey})

        return self._request(self.__businessLicenseUrl, data)

    def vcode(self, image, options=None):
        """
            验证码识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        data.update({"apiKey": self._apiKey, "secretKey": self._secretKey})

        return self._request(self.__vCodeUrl, data)

    
    

     