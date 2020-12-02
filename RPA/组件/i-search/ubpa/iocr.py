# -*- coding:utf-8 -*-
'''
Created on 2018-2-3

@author: Wu.Xin
使用百度ocr
'''
from aip import AipOcr
import ctypes
import json
from ubpa import encrypt
from ubpa.ilog import ILog
from ubpa.iip.ocr import IipOcr
from PIL import Image
import pytesseract
import requests
from os.path import join, dirname


__logger = ILog(__file__)

def general_recognize(image_path="", apiKey="", secretKey=""):
    '''
    :param image_path: 传入图片地址
    :param apiKey:
    :param secretKey:
    :return: 通用文字识别, 返回文本     错误返回:  1	    服务器内部错误
                                                2	    服务暂不可用
                                                100	    无效的access_token参数，请检查后重新尝试
                                                110	    access_token无效
                                                111	    access token过期
                                                216201	上传的图片格式错误，现阶段我们支持的图片格式为：PNG、JPG、JPEG、BMP，请进行转码或更换图片
                                                216202	上传的图片大小错误，现阶段我们支持的图片大小为：base64编码后小于4M，分辨率不高于4096*4096，请重新上传图片
                                                282810	图像识别错误
    '''
    __logger.info(u"Ready to execute [general_recognize]")
    text=""
    try:
        client = get_client(apiKey, secretKey)
        image = get_file_content(image_path)
        data = client.basicGeneral(image)
        __list=data['words_result']
        list_str = []
        for index in range(len(__list)):
            dict_str=__list[index]
            list_str.append(dict_str['words'])
        text = ''.join(list_str)
        return text
    except Exception as e:
        __logger.error('First recognition error:'+str(data))
        raise e
        # bd_general_recognize(image_path)

    finally:
        __logger.debug('[general_recognize] result :[' + text + ']')
        __logger.echo_msg(u"end execute [general_recognize]")



def idcard_recognize(image_path="",idCardSide="", apiKey="", secretKey=""):
    '''
    :param image_path: 传入图片地址
    :param idCardSide: 正面 or 反面
    :param apiKey:
    :param secretKey:
    :return: 获取身份证信息   错误返回:   1	    服务器内部错误
                                        2	    服务暂不可用
                                        100	    无效的access_token参数，请检查后重新尝试
                                        110	    access_token无效
                                        111	    access token过期
                                        216201	上传的图片格式错误，现阶段我们支持的图片格式为：PNG、JPG、JPEG、BMP，请进行转码或更换图片
                                        216202	上传的图片大小错误，现阶段我们支持的图片大小为：base64编码后小于4M，分辨率不高于4096*4096，请重新上传图片
                                        216633	识别身份证错误，出现此问题的原因一般为：您上传了非身份证图片或您上传的身份证图片不完整
                                        282810	图像识别错误
    '''
    __logger.info(u"Ready to execute[idcard_recognize]")
    dict_str = {}
    options={}
    options['id_card_side']=idCardSide
    try:
        client = get_client(apiKey, secretKey)
        image = get_file_content(image_path)
        data= client.idcard(image,options)
        if idCardSide == "front":
            if ('姓名' in data['words_result'].keys())==True:
                dict_str['name']=str(data['words_result']['姓名']['words'])
            else:
                dict_str['name']= ''
            if ('民族' in data['words_result'].keys())==True:
                dict_str['nationality']= str(data['words_result']['民族']['words'])
            else:
                dict_str['nationality']= ''
            if ('住址' in data['words_result'].keys())==True:
                dict_str['address']=str(data['words_result']['住址']['words'])
            else:
                dict_str['address']= ''
            if ('公民身份号码' in data['words_result'].keys())==True:
                dict_str['idno']=str(data['words_result']['公民身份号码']['words'])
            else:
                dict_str['idno']= ''
            if ('出生' in data['words_result'].keys())==True:
                dict_str['birthdate']=str(data['words_result']['出生']['words'])
            else:
                dict_str['birthdate']= ''
            if ('性别' in data['words_result'].keys())==True:
                dict_str['gender']= str(data['words_result']['性别']['words'])
            else:
                dict_str['gender']= ''

        else:
            if ('签发日期' in data['words_result'].keys())==True:
                dict_str['date_b']= str(data['words_result']['签发日期']['words'])
            else:
                dict_str['date_b']= ''
            if ('失效日期' in data['words_result'].keys())==True:
                dict_str['date_e']= str(data['words_result']['失效日期']['words'])
            else:
                dict_str['date_e']= ''
            if ('签发机关' in data['words_result'].keys())==True:
                dict_str['organization']= str(data['words_result']['签发机关']['words'])
            else:
                dict_str['organization']= ''
        return dict_str
    except Exception as e:
        __logger.error('First recognition error:' + str(data))
        raise e
        # bd_idcard_recognize(image_path, idCardSide)
    finally:
        __logger.debug('[idcard_recognize] result :[' + str(dict_str) + ']')
        __logger.echo_msg(u"end execute [idcard_recognize]")



def business_license_recognize(image_path="", apiKey="", secretKey=""):
    '''
    :param image_path: 传入图片地址
    :param apiKey:
    :param secretKey:
    :return: 营业执照识别     错误返回:   1	    服务器内部错误
                                        2	    服务暂不可用
                                        100	    无效的access_token参数，请检查后重新尝试
                                        110	    access_token无效
                                        111	    access token过期
                                        216201	上传的图片格式错误，现阶段我们支持的图片格式为：PNG、JPG、JPEG、BMP，请进行转码或更换图片
                                        216202	上传的图片大小错误，现阶段我们支持的图片大小为：base64编码后小于4M，分辨率不高于4096*4096，请重新上传图片
                                        282810	图像识别错误
    '''
    __logger.info(u"Ready to execute[business_license_recognize]")
    dict_str = {}
    try:
        client = get_client(apiKey, secretKey)
        image = get_file_content(image_path)
        data= client.businessLicense(image)
        if ('社会信用代码' in data['words_result'].keys())==True:
            dict_str['socialCreditCode']=str(data['words_result']['社会信用代码']['words'])
        else:
            dict_str['socialCreditCode']= ''
        if ('组成形式' in data['words_result'].keys())==True:
            dict_str['组成形式']= str(data['words_result']['组成形式']['words'])
        else:
            dict_str['组成形式'] = ''
        if ('法人' in data['words_result'].keys()) == True:
            dict_str['legal entity'] = str(data['words_result']['法人']['words'])
        else:
            dict_str['legal entity'] = ''
        if ('成立日期' in data['words_result'].keys()) == True:
            dict_str['date_b'] = str(data['words_result']['成立日期']['words'])
        else:
            dict_str['date_b'] = ''
        if ('注册资本' in data['words_result'].keys()) == True:
            dict_str['registered capital'] = str(data['words_result']['注册资本']['words'])
        else:
            dict_str['registered capital'] = ''
        if ('证件编号' in data['words_result'].keys()) == True:
            dict_str['ID number'] = str(data['words_result']['证件编号']['words'])
        else:
            dict_str['ID number'] = ''
        if ('地址' in data['words_result'].keys()) == True:
            dict_str['address'] = str(data['words_result']['地址']['words'])
        else:
            dict_str['address'] = ''
        if ('单位名称' in data['words_result'].keys()) == True:
            dict_str['organization'] = str(data['words_result']['单位名称']['words'])
        else:
            dict_str['organization'] = ''
        if ('类型' in data['words_result'].keys()) == True:
            dict_str['type'] = str(data['words_result']['类型']['words'])
        else:
            dict_str['type'] = ''
        if ('有效期' in data['words_result'].keys()) == True:
            dict_str['valid'] = str(data['words_result']['有效期']['words'])
        else:
            dict_str['valid'] = ''

        return dict_str
    except Exception as e:
        __logger.error('First recognition error:' + str(data))
        raise e
        # bd_business_license_recognize(image_path)
    finally:
        __logger.debug('[business_license_recognize] result :[' + str(dict_str) + ']')
        __logger.echo_msg(u"end execute[business_license_recognize]")




def vcode_recognize(image_path="", code_type="5000", apiKey="", secretKey=""):
    '''
    :param image_path: 传入图片地址
    :param code_type: 验证码默认值 5000
    :param apiKey:
    :param secretKey:
    :return:  验证码识别   返回代号对应示意  1004	4位英文数字
                                          1005	5位英文数字
                                          1006	6位英文数字
                                          2002	2位纯汉字
                                          2004	4位纯汉字
                                          3004	4位纯英文
                                          3005	5位纯英文
                                          3006	6位纯英文
                                          4004	4位纯数字
                                          4005	5位纯数字
                                          1000	不定长英文数字
                                          2000	不定长纯汉字
                                          3000	不定长纯英文
                                          4000	不定长纯数字
                                          5000	不定长汉字英文数字、符号、空格
                                          8000	滑动验证码
                                          8001	坐标题
    '''
    __logger.info(u"Ready to execute[vCode_recognize]")
    options={}
    options["code_type"]=code_type
    result = ''
    data = {}
    data["result"] = ''
    try:
        client = get_client(apiKey, secretKey)
        image = get_file_content(image_path)
        data = client.vcode(image,options)
        result =data["result"]
        return result

    except Exception as e:
        __logger.error('First recognition error:' + str(data))
        raise e
    finally:
        __logger.debug('[vcode_recognize] result :[' + result + ']')
        __logger.echo_msg(u"end execute[vcode_recognize]")



def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def get_client(API_Key, Secret_Key):
    # API_Key = "dinga59d519024c5b9bd"
    # Secret_Key = "MTV1heO94n-PPTf5Bcm99YzvW_nwGTUwFpWM30RWK5dp9hzLHSBCDg_nY9tMK7ts"
    return IipOcr(API_Key, Secret_Key)


APP_ID = "MDQ2NSojIyoxMTI3"
API_KEY = "zeTVnSUQweWw3T0YqIwIyp2U2dDTld6NlNJTmx"
SECRET_KEY = "RUdVMWg4d1pPc011Z3FxUyojIypqZ2F2SFVtZkxPSDI0dk5D"


def bd_general_recognize(image_path=""):
    '''
        general_recognize(image_path="") -> str

        功能:
           通用识别
        参数:
          image_path: 需要识别的图片路径.
        返回:
              识别得到的字符串text.
        例子:
        general_recognize(image_path=r"c:\cc.png") -> "这是一串字符串"
    '''
    # __logger.info(u"Ready to execute[bd_general_recognize]")
    text=""
    try:
        client = bd_get_client()
        image = bd_get_file_content(image_path)
        data = client.basicGeneral(image)
        data_dict = json.loads(json.dumps(data))
        __list=data_dict['words_result']
        list_str = []
        for index in range(len(__list)):
            dict_str=__list[index]
            list_str.append(dict_str['words'])

        text = '\n'.join(list_str)
        return text
    except Exception as e:
        raise e
    finally:
        # __logger.debug('[bd_general_recognize] result :[' + text + ']')
        # __logger.echo_msg(u"end execute [bd_general_recognize]")
        pass



def bd_idcard_recognize(image_path="",idCardSide=""):

    '''
        idcard_recognize(image_path="",idCardSide="") -> dict{}

        功能:
           身份证识别
        参数:
            image_path: 需要识别的图片路径.
            idCardSide: 图片正反面，正面front;反面back
        返回:
              识别得到的字典dict.
        例子:
        idcard_recognize(image_path="c:\cc.png",idCardSide="front") -> {'address': '盛顿市中心区宾夕法尼亚大街1600号Whitehouse', 'id': '1234567890', 'birth': '19610804', 'name': '贝拉克·奥巴马', 'sex': '男', 'nation': '汉'}
    '''
    # __logger.info(u"Ready to execute[bd_idcard_recognize]")
    dict_str = {}
    try:
        client = bd_get_client()
        image = bd_get_file_content(image_path)
        data= client.idcard(image,idCardSide)
        data_dict = json.loads(json.dumps(data))
        if idCardSide=="front":
            if ('住址' in data_dict['words_result'].keys())==True:
                dict_str['address']=str(data_dict['words_result']['住址']['words'])
            else:
                dict_str['address']= ''
            if ('公民身份号码' in data_dict['words_result'].keys())==True:
                dict_str['id']= str(data_dict['words_result']['公民身份号码']['words'])
            else:
                dict_str['id']= ''
            if ('出生' in data_dict['words_result'].keys())==True:
                dict_str['birth']=str(data_dict['words_result']['出生']['words'])
            else:
                dict_str['birth']= ''
            if ('姓名' in data_dict['words_result'].keys())==True:
                dict_str['name']=str(data_dict['words_result']['姓名']['words'])
            else:
                dict_str['name']= ''
            if ('性别' in data_dict['words_result'].keys())==True:
                dict_str['sex']=str(data_dict['words_result']['性别']['words'])
            else:
                dict_str['sex']= ''
            if ('民族' in data_dict['words_result'].keys())==True:
                dict_str['nation']= str(data_dict['words_result']['民族']['words'])
            else:
                dict_str['nation']= ''

        else:

            if ('签发日期' in data_dict['words_result'].keys())==True:
                dict_str['date_b']= str(data_dict['words_result']['签发日期']['words'])
            else:
                dict_str['date_b']= ''
            if ('失效日期' in data_dict['words_result'].keys())==True:
                dict_str['date_e']= str(data_dict['words_result']['失效日期']['words'])
            else:
                dict_str['date_e']= ''
            if ('签发机关' in data_dict['words_result'].keys())==True:
                dict_str['organization']= str(data_dict['words_result']['签发机关']['words'])
            else:
                dict_str['organization']= ''
        return dict_str
    except Exception as e:
        raise e
    finally:
        # __logger.debug('[bd_idcard_recognize] result : [' + str(dict_str) + ']')
        # __logger.echo_msg(u"end execute [bd_idcard_recognize]")
        pass


def bd_business_license_recognize(image_path=""):

    '''
        business_license_recognize(image_path="") -> dict
        功能:
           营业执照识别
        参数:
          image_path: 需要识别的图片路径.
        返回:
            识别得到的字典dict.
        例子:
        business_license_recognize(image_path=r"c:\cc.png") -> {'organization': '深圳市特盛科技有限公司', 'legalperson': '董有彩', 'address': '北京市', 'limited': '无', 'id': '440301105957424', 'socialCreditCode': '无'}
    '''
    # __logger.info(u"Ready to execute[bd_business_license_recognize]")
    dict_str = {}
    try:
        client = bd_get_client()
        image = bd_get_file_content(image_path)
        data= client.businessLicense(image)
        data_dict = json.loads(json.dumps(data))
        if ('单位名称' in data_dict['words_result'].keys()) == True:
            dict_str['organization'] = str(data_dict['words_result']['单位名称']['words'])
        else:
            dict_str['organization'] = ''
        if ('法人' in data_dict['words_result'].keys()) == True:
            dict_str['legalperson'] = str(data_dict['words_result']['法人']['words'])
        else:
            dict_str['legalperson'] = ''
        if ('地址' in data_dict['words_result'].keys()) == True:
            dict_str['address'] = str(data_dict['words_result']['地址']['words'])
        else:
            dict_str['address'] = ''
        if ('有效期' in data_dict['words_result'].keys()) == True:
            dict_str['limited'] = str(data_dict['words_result']['有效期']['words'])
        else:
            dict_str['limited'] = ''
        if ('证件编号' in data_dict['words_result'].keys()) == True:
            dict_str['id'] = str(data_dict['words_result']['证件编号']['words'])
        else:
            dict_str['id'] = ''
        if ('社会信用代码' in data_dict['words_result'].keys()) == True:
            dict_str['socialCreditCode'] = str(data_dict['words_result']['社会信用代码']['words'])
        else:
            dict_str['socialCreditCode'] = ''

        return dict_str
    except Exception as e:
        raise e
    finally:
        # __logger.debug('[bd_business_license_recognize] result :[' + str(dict_str) + ']')
        # __logger.echo_msg(u"end execute [bd_business_license_recognize]")
        pass

def bd_qr_code_recognize(image_path=""):

    '''
        qr_Code_recognize(image_path="") -> text
        功能:
           二维码识别
        参数:
          image_path: 需要识别的图片路径.
        返回:
            识别得到的字符串.
        例子:
        qr_Code_recognize(image_path=r"c:\cc.png") -> "这是一串字符串"
    '''
    # __logger.info(u"Ready to execute[bd_qr_code_recognize]")
    text = ""
    list_str=[]
    try:
        client = bd_get_client()
        image = bd_get_file_content(image_path)
        data = client.qr_Code(image)
        data_dict = json.loads(json.dumps(data))
        __list = data_dict['codes_result']
        for index in range(len(__list)):
            dict_str = __list[index]
            if dict_str['type'] == 'QR_CODE':
                list_str = dict_str['text']

        text = '\n'.join(list_str)
        return text
    except Exception as e:
        raise e
    finally:
        # __logger.debug('[bd_qr_code_recognize] result:[' + text + ']')
        # __logger.echo_msg(u"end execute [bd_qr_code_recognize]")
        pass


def bd_get_client():
    return AipOcr(encrypt.decrypt(APP_ID), encrypt.decrypt(API_KEY), encrypt.decrypt(SECRET_KEY))

def bd_get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()






def _request(self, url, data, headers=None):
        """
            self._request('', {})
        """
        try:
            result = self._validate(url, data)
            if result != True:
                return result

            authObj = self._auth()
            params = self._getParams(authObj)

            data = self._proccessRequest(url, params, data, headers)
            headers = self._getAuthHeaders('POST', url, params, headers)
            response = self.__client.post(url, data=data, params=params,
                            headers=headers, verify=False, timeout=(
                                self.__connectTimeout,
                                self.__socketTimeout,
                            ), proxies=self._proxies
                        )
            obj = self._proccessResult(response.content)

            if not self._isCloudUser and obj.get('error_code', '') == 110:
                authObj = self._auth(True)
                params = self._getParams(authObj)
                response = self.__client.post(url, data=data, params=params,
                                headers=headers, verify=False, timeout=(
                                    self.__connectTimeout,
                                    self.__socketTimeout,
                                ), proxies=self._proxies
                            )
                obj = self._proccessResult(response.content)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as e:
            return {
                'error_code': 'SDK108',
                'error_msg': 'connection or read data timeout',
            }

        return obj

def get_tesseract_ocr(img_path,lang=None):
    txt = None
    try:
        image = Image.open(img_path)
        txt = pytesseract.image_to_string(image,lang=lang)
        if txt != None:
            txt = txt.replace(' ','')
        #print(txt)

    except Exception as e:
        raise e
    finally:
        return txt

def get_ydm_code(filename, codetype=5001, timeout=30):
    '''
    '''
#     YDMApi = windll.LoadLibrary(r'd:\svn\isa\branches\ueba_5.0\makesetup\CdaSetupDate\bin\yundamaAPI.dll')
    YDMApi = ctypes.windll.LoadLibrary("../../bin/yundamaAPI.dll")
    result = ctypes.c_char_p(b"                              ")
    username = b"isearch"
    password = "hcmNoKiMIyppc2V="
    password = encrypt.decrypt(password)
    password = bytes(password,encoding='utf-8')
    appId = 5364
    appKey = b"54b9ebb03b894bad4f52e4f3553edffb"
#     filename = b"C:\Users\ibm\Desktop\dynamicPassword.jpg"
    filename = filename.encode(encoding="utf-8")
    captchaId = YDMApi.YDM_EasyDecodeByPath(username, password, appId, appKey, filename, codetype, timeout, result)

    __logger.debug("recognize:ID:%d，result:%s" % (captchaId, result.value))
    return str(result.value, encoding="utf-8")

YDMApi = ctypes.windll.LoadLibrary("../../bin/yundamaAPI.dll")
def get_yundama_balance():

    YDMApi.YDM_SetAppInfo(5364, b"54b9ebb03b894bad4f52e4f3553edffb")
    YDMApi.YDM_Login(b"isearch", b"i-search")

    return YDMApi.YDM_GetBalance(b"isearch", b"i-search")

# print(encrypt.decrypt(APP_ID))
# print(encrypt.decrypt(API_KEY))
# print(encrypt.decrypt(SECRET_KEY))
# abc = get_ydm_code("C:/Users/ibm/Desktop/1.PNG")
# print(abc)
# print(abc,'dddd',code)
# get_ydm_code(b"C:/Users/ibm/Desktop/33.png")
# APP_ID = "115"   API_KEY = "vSgCNWz6SINlsy5gID0yl7OF"   SECRET_KEY = "jgavHUmfLOH24vNCEGU1h8wZOsMugqqS"

dc_dll = ctypes.windll.LoadLibrary('../../bin/dc.dll')
class CHAORENCode:

    def __init__(self, user, pwd, softId="0"):  ##softId 软件ID 缺省为0,作者务必提交softId,已保证分成
        self.user = user.encode(encoding="utf-8")
        self.pwd = pwd.encode(encoding="utf-8")
        self.softId = softId.encode(encoding="utf-8")


    def getUserInfo(self):
        '''
        :return: 获取账号剩余点数  返回"-1"----网络错误  返回"-5"----账户密码错误
        '''
        p = dc_dll.GetUserInfo(self.user, self.pwd)
        if p:
            return ctypes.string_at(p, -1).decode()
        return ''


def get_chaoren_balance():
    username = "isearch"
    password = "is1arch-u1ba"

    user_info = dc_dll.GetUserInfo(username, password)

    return ctypes.string_at(user_info, -1).decode('utf-8')

