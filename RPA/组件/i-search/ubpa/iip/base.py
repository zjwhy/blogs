# -*- coding: utf-8 -*-

"""
    IipOcrBase
"""
import base64
import datetime
import hashlib
import hmac
import json
import sys
import requests
import time 
from urllib.parse import quote
from urllib.parse import urlencode
from urllib.parse import urlparse



class IipOcrBase(object):
    """
        IipOcrBase
    """ 

    def __init__(self,  apiKey, secretKey):
        """
            IipOcrBase( apiKey, secretKey)
        """

        #self._appId = appId.strip()
        self._apiKey = apiKey.strip()
        self._secretKey = secretKey.strip()
        self._authObj = {}
        self._isCloudUser = None
        self.__client = requests
        self.__connectTimeout = 60.0
        self.__socketTimeout = 60.0
        self._proxies = {}
        self.__version = '2_1_0'
 
    def _request(self, url, data, headers=None):
        """
            self._request('', {})
        """
        try:
            result = self._validate(url, data) 
            if result != True:
                return result
            data = self._proccessRequest(data)
            headers = self._getAuthHeaders(headers)
            response = self.__client.post(url, data=data, headers=headers, verify=False,
                                          timeout=(self.__connectTimeout,self.__socketTimeout,), proxies=self._proxies)
            obj = self._proccessResult(response.content)

        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as e:
            return {
                'error_code': 'SDK108',
                'error_msg': 'connection or read data timeout',
            }
 
        return obj

    def _validate(self, url, data):
        """
            validate
        """
        return True

    def _getAuthHeaders(self, headers=None):
        """
              headers
        """
        headers = headers or {}
        headers['Content-Type'] = r'text/html'
        return headers

    def _proccessRequest(self,data):
        """
            参数处理
        """
        return json.dumps(data)


    def _proccessResult(self, content):
        """
            format result
        """ 
        if sys.version_info.major == 2:
            return json.loads(content) or {}
        else:
            return json.loads(content.decode()) or {}

    
    def _getParams(self, authObj):
        """
            api request http url params
        """

        params = {}

        if self._isCloudUser == False:
            params['access_token'] = authObj['access_token']

        return params


