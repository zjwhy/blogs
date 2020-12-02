# -*- coding:utf-8 -*-
import json
import sys

import requests
import configparser
import os
import ubpa.encrypt as enc
from ubpa.iconstant import *
import time
import json

from urllib import parse
import hmac
import base64
from hashlib import sha256
from ubpa.ilog import ILog

logger = ILog(__file__)


class PlatformRequest(object):


    def __init__(self, timeout):
        self.__authObj = {}
        self.__isCloudUser = None
        self.__client = requests
        self.__connectTimeout = timeout
        self.__socketTimeout = timeout
        self.__proxies = {}
        self.__version = '2_1_0'
 

    def _getPlatformUrl(self):
        try:
            config = configparser.ConfigParser()
            ini_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")) + os.sep + "config" + os.sep + "UEBAOption.ini"
            config.read_file(open(ini_path))

            addr = config.get("SERVER_INFO", "MainServer")
            port = config.get("SERVER_INFO", "WebServicePort")

            return "http://" + addr + ":" + port
        except Exception as e:
            raise e
 
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
                                          timeout=(self.__socketTimeout, self.__connectTimeout), proxies=self.__proxies)

            obj = self._proccessResult(response.content)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as e:
            return {
                'code': 'SDK108',
                'errMsg': 'connection or read data timeout',
                'status': 1
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
        if headers == None:
            headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}

        return headers

    def _proccessRequest(self, data):
        """
            参数处理
        """
        return 'param=' + json.dumps(data)


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


    def get_token(self,timeout, timestamp):
        try:
            param = {
                "tenant_id": "xxx",
                "appid": "appid",
                "secret": "secret"
            }

            sign_str = "param=" + json.dumps(param, ensure_ascii=False) + "&timestamp=" + timestamp

            sign = self.get_sign(sign_str)

            url = self._getPlatformUrl() + "/rapi/call.action?action=get-token&timestamp=" + timestamp + "&sign=" + sign

            return self._request(url, param, timeout)

        except Exception as e:
            raise e



    def get_sign(self,sign_str):
        try:
            str2 = parse.quote(sign_str)

            byte_key = bytes("isearch", encoding="utf-8")
            byte_str2 = bytes(str2, encoding="utf-8")
            hn = hmac.new(byte_key, byte_str2, digestmod=sha256)
            hh = hn.hexdigest()

            str3 = base64.b64encode(bytes(hh, encoding="utf-8"))
            return str(str3, "utf-8")
        except Exception as e:
            raise e



class TagsSender(PlatformRequest):
    
    def __init__(self):
        pass
    
    
    def sendTags(self,tags):
        pass
    


    
class AssetHandler(PlatformRequest):
    
    def __init__(self, robot_no, timeout):
        self.platform = self._getPlatformUrl()
        self.robot_no = robot_no
        self.__getAssetUrl = self.platform + "/rapi/call.action?action=get-vars"
        self.__setAssetUrl = self.platform + "/rapi/call.action?action=set-var"
        super().__init__(timeout)


    def getAsset(self, name):
        logger.debug('start getAsset')
        value = ""
        try:
            p = {
                "var_name": name,
                "robot_no": self.robot_no
            }
            timestamp = str(int(time.time()))

            # token = self.get_token(timeout, timestamp)
            # print(token)


            sign_str = "action=get-vars&param=" + json.dumps(p) + "&timestamp=" + timestamp
            sign = self.get_sign(sign_str)

            get_url = self.__getAssetUrl + "&timestamp=" + timestamp + "&sign=" + sign
            asset_data = self._request(get_url, p)
            if 0 == asset_data["code"]:
                value = asset_data["result"]["var_value"]
                if "yes" == asset_data["result"]["is_python_exp"]:
                    value = json.loads(value, encoding="utf-8")
                    return value

                if "passwd" == asset_data["result"]["var_type"]:
                    value = enc.encrypt(str(value))

                return value
            else:
                logger.debug('getAsset error:' + str(asset_data))
                return value
        except Exception as e:
            raise e
        finally:
            logger.debug('finish getAsset' + str(value))
            # pass


    def setAsset(self, name, value):
        logger.debug('start setAsset')
        try:

            if isinstance(value, dict):
                value = json.dumps(value, ensure_ascii=False)
            elif isinstance(value, str):
                value = enc.decrypt(value)

            p = {
                "var_name": name,
                "var_value": value,
                "var_type": "",
                "robot_no": self.robot_no,
                "is_python_exp": ""
            }
            timestamp = str(int(time.time()))

            # token = self.get_token(timeout, timestamp)

            sign_str = "action=set-var&param=" + json.dumps(p) + "&timestamp=" + timestamp
            sign = self.get_sign(sign_str)

            set_url = self.__setAssetUrl + "&timestamp=" + timestamp + "&sign=" + sign

            asset_data = self._request(set_url, p)
            if 0 == asset_data["code"]:
                return True
            else:
                logger.debug('setAsset error:' + str(asset_data))
                return False
        except Exception as e:
            raise e
        finally:
            logger.debug('finish setAsset')
            # pass


    
    
class QueueHandler(PlatformRequest):
    
    def __init__(self, robot_no, job_no, proc_no, timeout):
        self.plateform = self._getPlatformUrl()
        self.robot_no = robot_no
        self.job_no = job_no
        self.proc_no = proc_no
        self._addItems = self.plateform + '/rapi/call.action?action=add-queue-item'
        self._queryItems = self.plateform + '/rapi/call.action?action=get-queue-items'
        self._delItems = self.plateform + '/rapi/call.action?action=del-queue-item'
        self._popItem = self.plateform + '/rapi/call.action?action=pop-queue-item'
        self._setItemStatus = self.plateform + '/rapi/call.action?action=update-queue-item'
        super().__init__(timeout)


    def addItems(self, name, items, priority, deadline):
        logger.debug('start addItems')
        try:

            p = {
                "queue_name": name,
                "deadline": deadline,
                "priority": priority,
                "status": "pending",
                "robot_no": self.robot_no,
                "job_no": self.job_no,
                "proc_no": self.proc_no
            }
            if isinstance(items, dict):
                p.update(items)

            timestamp = str(int(time.time()))

            sign_str = "action=add-queue-item&param=" + json.dumps(p) + "&timestamp=" + timestamp
            sign = self.get_sign(sign_str)

            additems_url = self._addItems + "&timestamp=" + timestamp + "&sign=" + sign

            result_data = self._request(additems_url, p)
            if 0 == result_data["code"]:
                return True
            else:
                logger.debug('addItems error:' + str(result_data))
                return False
        except Exception as e:
            raise e
        finally:
            logger.debug('finish addItems')
            # pass

    
    def queryItems(self, name, s_time, e_time, status, priority, es_filter):
        logger.debug('start queryItems')
        value = []
        try:
            p = {
                "queue_name": name,
                "from": s_time,
                "to": e_time,
                "status": status,
                "priority": priority,
                "filter": es_filter,
                "robot_no": self.robot_no
            }

            timestamp = str(int(time.time()))

            sign_str = "action=get-queue-items&param=" + json.dumps(p) + "&timestamp=" + timestamp
            sign = self.get_sign(sign_str)

            queryitems_url = self._queryItems + "&timestamp=" + timestamp + "&sign=" + sign

            result_data = self._request(queryitems_url, p)
            if 0 == result_data["code"]:
                value = result_data["result"]
                return value
            else:
                logger.debug('queryItems error:' + str(result_data))
                return value
        except Exception as e:
            raise e
        finally:
            logger.debug('finish queryItems:' + str(value))
            # pass

    
    def delItems(self, name, items):
        logger.debug('start delItems')
        try:

            p = {
                "queue_name": name,
                "items": items,
                "robot_no": self.robot_no,
                "job_no": self.job_no,
                "proc_no": self.proc_no
            }
            timestamp = str(int(time.time()))

            sign_str = "action=del-queue-item&param=" + json.dumps(p) + "&timestamp=" + timestamp
            sign = self.get_sign(sign_str)

            delitems_url = self._delItems + "&timestamp=" + timestamp + "&sign=" + sign

            result_data = self._request(delitems_url, p)
            if 0 == result_data["code"]:
                return True
            else:
                logger.debug('delItems error:' + str(result_data))
                return False
        except Exception as e:
            raise e
        finally:
            logger.debug('finish delItems')
            # pass

    
    def popItem(self, name):
        logger.debug('start popItem')
        value = {}
        try:

            p = {
                "queue_name": name,
                "robot_no": self.robot_no,
                "job_no": self.job_no,
                "proc_no": self.proc_no
            }

            timestamp = str(int(time.time()))

            sign_str = "action=pop-queue-item&param=" + json.dumps(p) + "&timestamp=" + timestamp
            sign = self.get_sign(sign_str)

            popitem_url = self._popItem + "&timestamp=" + timestamp + "&sign=" + sign

            result_data = self._request(popitem_url, p)
            if 0 == result_data["code"]:
                value = result_data["result"]
                return value
            else:
                logger.debug('popItem error:' + str(result_data))
                return value
        except Exception as e:
            raise e
        finally:
            logger.debug('finish popItem:' + str(value))
            # pass

    
    def setItemStatus(self, name, items, status, fail_desc):
        logger.debug('start setItemStatus')
        try:

            p = {
                "queue_name": name,
                "status": status,
                "fail_desc": fail_desc,
                "proc_no": self.proc_no,
                "robot_no": self.robot_no,
                "job_no": self.job_no
            }

            if isinstance(items, dict):
                item_no = items.get('item_no', None)
                if item_no != None:
                    item = {"item_no": item_no}
                    p.update(item)
            elif isinstance(items, str):
                item = {"item_no": items}
                p.update(item)

            timestamp = str(int(time.time()))

            sign_str = "action=update-queue-item&param=" + json.dumps(p) + "&timestamp=" + timestamp
            sign = self.get_sign(sign_str)

            setitemstatus_url = self._setItemStatus + "&timestamp=" + timestamp + "&sign=" + sign

            result_data = self._request(setitemstatus_url, p)
            if 0 == result_data["code"]:
                return True
            else:
                logger.debug('setItemStatus error:' + str(result_data))
                return False
        except Exception as e:
            raise e
        finally:
            logger.debug('finish setItemStatus')
            # pass



def getAsset(name, robot_no, timeout=WAIT_FOR):
    try:
        asset = AssetHandler(robot_no, timeout)
        return asset.getAsset(name)
    except Exception as e:
        raise e

def setAsset(name, value, robot_no, timeout=WAIT_FOR):
    try:
        asset = AssetHandler(robot_no, timeout)
        return asset.setAsset(name, value)
    except Exception as e:
        raise e


def addItems(name, items, robot_no, job_no, proc_no, priority="normal", deadline="", timeout=WAIT_FOR):
    try:
        queue = QueueHandler(robot_no, job_no, proc_no, timeout)
        return queue.addItems(name, items, priority, deadline)
    except Exception as e:
        raise e

def queryItems(name, robot_no, job_no, proc_no, s_time=None, e_time=None, status=None, priority=None, es_filter=None, timeout=WAIT_FOR):
    try:
        queue = QueueHandler(robot_no, job_no, proc_no, timeout)
        return queue.queryItems(name, s_time, e_time, status, priority, es_filter)
    except Exception as e:
        raise e

def delItems(name, items, robot_no, job_no, proc_no, timeout=WAIT_FOR):
    try:
        queue = QueueHandler(robot_no, job_no, proc_no, timeout)
        return queue.delItems(name, items)
    except Exception as e:
        raise e

def popItem(name, robot_no, job_no, proc_no, timeout=WAIT_FOR):
    try:
        queue = QueueHandler(robot_no, job_no, proc_no, timeout)
        return queue.popItem(name)
    except Exception as e:
        raise e

def setItemStatus(name, items, status, robot_no, job_no, proc_no, desc='', timeout=WAIT_FOR):
    try:
        queue = QueueHandler(robot_no, job_no, proc_no, timeout)
        return queue.setItemStatus(name, items, status, desc)
    except Exception as e:
        raise e


# if __name__ == '__main__':
#     pass
#     res = addItems("123", {"u1": "i1"}, 2, 123, 456, "normal", "2019-04-20 12:15", 30)
#     print(res)

    # res = queryItems("123", "", "", "pending", "normal", "", 2, 123, 456, 40)
    # print(res)

    # res = popItem("123", 2, 123, 456, 62)
    # print(res)

    # res = setItemStatus("123", "da5a4462639b4eacb49f6ecc5713f9ac", "pending", "", 2, 123, 456)
    # print(res)

    # res = getAsset("小明", "zhaomengru1220@005056C00001", 333)
    # print(res)

    # res = setAsset("333", "text", "rere", "123@456", "no", 985)
    # print(res)