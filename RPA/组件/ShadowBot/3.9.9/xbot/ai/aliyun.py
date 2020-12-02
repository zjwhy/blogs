import base64, urllib, json
from .aibase import AIBase
from io import BytesIO

class AliyunAI(AIBase):
    '''
    阿里云OCR模块
    '''

    def __init__(self, app_code, edition='ocr_general'):
        '''
        创建AliyunAI对象
        * @param app_code, 阿里云OCR开发编码
        * @param edition, 阿里云通用场景文字识别分两个版本：
            * `'ocr_general'`,  印刷文字识别-通用文字识别/OCR文字识别
            * `'advanced'`,     通用文字识别－高精版OCR文字识别
        '''
        
        self.app_code = app_code
        
        if edition not in ['ocr_general', 'advanced']:
            edition = 'ocr_general'
        self.edition = edition


    def _recognize_text(self, image):
        ocr_result = self._request_server_to_ocr(image)
        return [item['word'] for item in ocr_result]


    def _recognize_text_with_location(self, image):
        ocr_result = self._request_server_to_ocr(image)

        text_with_location_list = []
        for item in ocr_result:
            text = item['word']
            location = item['rect']
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

    # 请求阿里服务器，以获取图片的OCR识别结果
    def _request_server_to_ocr(self, image):
        '''
        官方Api文档：
        https://market.aliyun.com/products/57124001/cmapi020020.html?spm=5176.730005.productlist.d_cmapi020020.494d35243d2efP&innerSource=search_%E9%80%9A%E7%94%A8%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB#sku=yuncode1402000000
        https://market.aliyun.com/products/57124001/cmapi028554.html?spm=5176.730005.productlist.d_cmapi028554.494d35243d2efP&innerSource=search_%E9%80%9A%E7%94%A8%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB#sku=yuncode2255400000
        '''
        # 1、image => base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        image_base64 = str(base64.b64encode(buffered.getvalue()),'utf-8')
        data = json.dumps({'image':image_base64}).encode(encoding='UTF8')

        # 2、HTTP Header
        headers = {}
        headers['Authorization'] = 'APPCODE ' + self.app_code
        headers['Content-Type'] = 'application/json; charset=UTF-8'

        # 3、HTTP Request
        if self.edition=='ocr_general':
            url = 'https://tysbgpu.market.alicloudapi.com/api/predict/ocr_general'
        else:
            url = 'https://ocrapi-advanced.taobao.com/ocrservice/advanced'
        
        try:
            request = urllib.request.Request(url=url, headers=headers, data=data)
            response = urllib.request.urlopen(request)        
            response_text = response.read().decode("utf8")
            return json.loads(response_text).get('ret', [])
        except urllib.error.HTTPError as e:
            raise ValueError('阿里云 OCR 识别错误，错误代码：' + e.msg)