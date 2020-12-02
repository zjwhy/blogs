import base64, urllib, json
from .aibase import AIBase
from io import BytesIO

class BaiduAI(AIBase):
    '''
    百度OCR模块
    '''
    

    def __init__(self, api_key, secret_key, edition='general'):
        '''
        创建BaiduAI对象
        * @param api_key, 百度Ocr开发密钥
        * @param secret_key, 百度Ocr连接密钥
        * @param edition, 百度通用场景文字识别分两个版本：
            * `'general'`,          标准版
            * `'accurate'`,         高精度版
        '''

        self.api_key = api_key
        self.secret_key = secret_key
        self._get_token()

        if edition not in ['general', 'accurate']:
            edition = 'general'
        self.edition = edition


    def _get_token(self):
        url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}'
        with urllib.request.urlopen(url) as f:
            ret = json.loads(f.read())
            error_desc = ret.get('error_description', None)
            if error_desc is not None:
                raise ValueError('不能获取百度Access Token，原因：' + error_desc)
            else:
                self.token = ret['access_token']


    def _recognize_text(self, image):
        ocr_result = self._request_server_to_ocr(image)
        return [item['words'] for item in ocr_result]
    

    def _recognize_text_with_location(self, image):
        ocr_result = self._request_server_to_ocr(image)

        text_with_location_list = []
        for item in ocr_result:
            text = item['words']
            location = item['location']
            text_with_location = {
                'text': text, 
                'location': {
                    'left': location['left'], 
                    'top': location['top'], 
                    'width': location['width'], 
                    'height': location['height']
                }
            }
            text_with_location_list.append(text_with_location)
        return text_with_location_list

    
    # 请求百度服务器，以获取图片的OCR识别结果
    def _request_server_to_ocr(self, image):
        '''
        官方Api文档：
        https://ai.baidu.com/ai-doc/OCR/zk3h7xz52
        '''
        # 1、image => base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        image_base64 = base64.b64encode(buffered.getvalue())
        data = urllib.parse.urlencode({"image":image_base64}).encode('utf-8')

        # 2、HTTP Header
        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        # 3、HTTP Request Url
        key = self.edition
        url = f'https://aip.baidubce.com/rest/2.0/ocr/v1/{key}?access_token={self.token}'
        
        # 4、HTTP Request
        request = urllib.request.Request(url=url, headers=headers, data=data)
        response = urllib.request.urlopen(request)
        response_text = response.read().decode("utf8")
        response_obj = json.loads(response_text)
        if response_obj.get('error_code', None) is not None:
            raise ValueError('百度 OCR 识别错误，原因：' + response_obj['error_msg'])

        return response_obj.get('words_result', [])