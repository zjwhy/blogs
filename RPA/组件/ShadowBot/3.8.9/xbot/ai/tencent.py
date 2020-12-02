import base64, urllib, json, time, datetime, hashlib, hmac
from .aibase import AIBase
from io import BytesIO
from datetime import datetime


class TencentAI(AIBase):
    '''
    腾讯OCR模块
    '''

    def __init__(self, secret_id, secret_key, edition='GeneralBasicOCR'):
        '''
        创建TencentAI对象
        * @param secret_id, 腾讯Ocr连接编号
        * @param secret_key, 腾讯Ocr连接密钥
        * @param edition, 腾讯通用场景文字识别分四个版本：
            * `'GeneralBasicOCR'`,      通用印刷体识别
            * `'GeneralAccurateOCR'`,   通用印刷体识别（高精度版）
            * `'GeneralEfficientOCR'`,  通用印刷体识别（精简版）
            * `'GeneralFastOCR'`,       通用印刷体识别（高速版）
        '''

        self.secret_id = secret_id
        self.secret_key = secret_key
        
        if edition not in ['GeneralBasicOCR', 'GeneralAccurateOCR', 'GeneralEfficientOCR', 'GeneralFastOCR']:
            edition = 'GeneralBasicOCR'
        self.edition = edition


    def _recognize_text(self, image):
        ocr_result = self._request_server_to_ocr(image)
        return [item['DetectedText'] for item in ocr_result]


    def _recognize_text_with_location(self, image):
        ocr_result = self._request_server_to_ocr(image)

        text_with_location_list = []
        for item in ocr_result:
            text = item['DetectedText']
            location = item['ItemPolygon']
            text_with_location = {
                'text': text, 
                'location': {
                    'left': location['X'], 
                    'top': location['Y'], 
                    'width': location['Width'], 
                    'height': location['Height']
                }
            }
            text_with_location_list.append(text_with_location)
        return text_with_location_list

    # 请求腾讯服务器，以获取图片的OCR识别结果
    def _request_server_to_ocr(self, image):
        '''
        官方Api文档：
        https://cloud.tencent.com/document/api/866/33526
        '''
        # 1、image => base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        image_base64 = str(base64.b64encode(buffered.getvalue()),'utf-8')

        # 2、
        service = "ocr"
        host = "ocr.tencentcloudapi.com"
        endpoint = "https://" + host
        region = "ap-guangzhou"
        action = self.edition
        version = "2018-11-19"
        algorithm = "TC3-HMAC-SHA256"
        timestamp = int(time.time())
        #timestamp = 1594195692
        date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
        params = {"ImageBase64": image_base64}

        # ************* 步骤 1：拼接规范请求串 *************
        http_request_method = "POST"
        canonical_uri = "/"
        canonical_querystring = ""
        ct = "application/json; charset=utf-8"
        payload = json.dumps(params)
        canonical_headers = "content-type:%s\nhost:%s\n" % (ct, host)
        signed_headers = "content-type;host"
        hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        canonical_request = (http_request_method + "\n" +
                            canonical_uri + "\n" +
                            canonical_querystring + "\n" +
                            canonical_headers + "\n" +
                            signed_headers + "\n" +
                            hashed_request_payload)

        # ************* 步骤 2：拼接待签名字符串 *************
        credential_scope = date + "/" + service + "/" + "tc3_request"
        hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
        string_to_sign = (algorithm + "\n" +
                        str(timestamp) + "\n" +
                        credential_scope + "\n" +
                        hashed_canonical_request)

        # ************* 步骤 3：计算签名 *************
        # 计算签名摘要函数
        def sign(key, msg):
            return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()
        secret_date = sign(("TC3" + self.secret_key).encode("utf-8"), date)
        secret_service = sign(secret_date, service)
        secret_signing = sign(secret_service, "tc3_request")
        signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

        # ************* 步骤 4：拼接 Authorization *************
        authorization = (algorithm + " " +
                        "Credential=" + self.secret_id + "/" + credential_scope + ", " +
                        "SignedHeaders=" + signed_headers + ", " +
                        "Signature=" + signature)

        # 3、HTTP Header
        headers = {}
        headers['X-TC-Action'] = action
        headers['X-TC-Region'] = region
        headers['X-TC-Timestamp'] = str(timestamp)
        headers['X-TC-Version'] = version
        headers['Authorization'] = authorization
        headers['host'] = host
        headers['Content-Type'] = ct
        headers['Accept'] = 'application/json'

        # 4、HTTP Request
        request = urllib.request.Request(url=endpoint, headers=headers, data=payload.encode('utf-8'))
        response = urllib.request.urlopen(request)        
        response_text = response.read().decode("utf8")

        # 5、Handle HTTP Reqsponse
        ret_response = json.loads(response_text).get('Response', None)

        if ret_response is None:
            raise ValueError("腾讯 OCR 文字识别返回的识别结果格式错误")

        ret_error = ret_response.get('Error', None)
        if ret_error is not None:
            raise ValueError("腾讯 OCR 文字识别错误，原因：" + ret_error["Message"])
        
        ret_text_detections = ret_response.get('TextDetections', None)
        if ret_text_detections is None:
            raise ValueError("腾讯 OCR 文字识别返回的识别结果格式错误")
        
        return ret_text_detections