from ._core import visual_action

import socket
import urllib
import urllib.request
import urllib.parse
import base64
import os

def string_to_dict(text, spliter):
    """
        text = "Key1=Value1\r\nKey2=Value2"
    """
    result = {}
    lines = text.split("\r\n")
    
    for line in lines:
        if line.find(spliter) != -1:
            (key, value) = line.strip().split(spliter, 1)
            result[key] = value

    return result

def get_http_file_name(response, orignal_url):
    file_name = response.info().get_filename()

    if file_name is None:
        file_name = os.path.basename(orignal_url)

    if file_name is None or file_name == '':
        file_name = 'index.html'

    return file_name

def save_to_file(path, data, encoding = None):
    file = None
    if isinstance(data, str) and encoding is not None:
        file = open(path, 'w', encoding=encoding)
    else:
        file = open(path, 'wb')
    file.write(data)
    file.close()

def process_url(url):
    url_parts = urllib.parse.urlparse(url)
    if url_parts[2] == '' and url_parts[3] == '' and url_parts[4] == '' and url_parts[5] == '':
        return url + '/'
    else:
        return url

class NoHTTPRedirectHandler(urllib.request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return fp
    http_error_301 = http_error_302

@visual_action
def http_request(**args):
    url                     = args['url']
    method                  = args['method']
    accept                  = args['accept']
    content_type            = args['content_type']
    custom_headers          = args['custom_headers']
    request_body            = args['request_body']
    connect_timeout_seconds = int(args['connect_timeout_seconds'])
    follow_redirection      = args['follow_redirection']
    fail_on_error_status    = args['fail_on_error_status']
    encode_request_body     = args['encode_request_body']
    user_agent              = args['user_agent']
    encoding                = args['encoding']
    http_authentication     = args['http_authentication']
    user_name               = args['user_name']
    password                = args['password']

    #保存方式
    return_data_save_way    = args["return_data_save_way"]
    file_save_way           = args["file_save_way"]
    folder_save_path        = args["folder_save_path"]
    file_save_path          = args["file_save_path"]

    # http headers
    headers = {}
    if accept:
        headers['Accept'] = accept
    if content_type:
        headers['Content-Type'] = content_type
    if custom_headers:
        headers.update(string_to_dict(custom_headers, ':'))
    if user_agent:
        headers['User-Agent'] = user_agent
    # https://www.v2ex.com/t/441114
    if http_authentication:
        plain_authorization = user_name + ':' + password
        headers['Authorization'] = 'Basic ' + str(base64.b64encode(plain_authorization.encode('utf-8')), 'utf-8')

    # http body
    body = None
    if request_body:
        if  encode_request_body:
            body = urllib.parse.quote(string=request_body).encode()
        else:
            body = request_body.encode()

    # 处理重定向
    if not follow_redirection:
        # 禁止重定向
        opener = urllib.request.build_opener(NoHTTPRedirectHandler)
        urllib.request.install_opener(opener)

    # 设置超时
    default_socket_timeout_senonds = socket.getdefaulttimeout()
    socket.setdefaulttimeout(connect_timeout_seconds)

    try:
        response_headers = {}
        response_page = ''
        response_status_code = 0

        # 请求
        real_url = urllib.request.quote(process_url(url), safe=";/?:@&=+$,")
        request_ = urllib.request.Request(url=real_url, headers=headers, data=body, method=method)
        response = urllib.request.urlopen(request_)

        #获取响应消息的协议头、网页（需解码）和状态码
        response_headers = {header:value for header, value in response.getheaders()}
        response_page = response.read()
                
        if encoding == "Auto-detect":
            response_charset = response.info().get_content_charset()
        else:
            response_charset = encoding

        if response_charset:
            response_page = response_page.decode(encoding=response_charset)

        response_status_code = response.status

        # 保存到本地文件
        if return_data_save_way == "save_to_disk":
            save_full_path = ""
            if file_save_way == "specify_folder":
                save_full_path = folder_save_path + "\\" + get_http_file_name(response, url)
            elif file_save_way == "specify_full_path":
                save_full_path = file_save_path

            save_to_file(save_full_path, response_page, response_charset)

    except BaseException as e:
        if fail_on_error_status:
            raise ValueError('HTTP 出错')
    finally:
        # 恢复默认超时
        socket.setdefaulttimeout(default_socket_timeout_senonds)

    return HttpResponse(response_status_code, response_headers, response_page)

@visual_action
def http_download(**args):
    url                     = args['url']
    method                  = args['method']
    post_parameters         = args['post_parameters']
    connect_timeout_seconds = int(args['connect_timeout_seconds'])
    follow_redirection      = args['follow_redirection']
    user_agent              = args['user_agent']
    encoding                = args['encoding']
    http_authentication     = args['http_authentication']
    user_name               = args['user_name']
    password                = args['password']

    #保存方式
    return_data_save_way    = args["return_data_save_way"]
    file_save_way           = args["file_save_way"]
    folder_save_path        = args["folder_save_path"]
    file_save_path          = args["file_save_path"]

    # http headers
    headers = {}
    if user_agent:
        headers['User-Agent'] = user_agent
    # https://www.v2ex.com/t/441114
    if http_authentication:
        plain_authorization = user_name + ':' + password
        headers['Authorization'] = 'Basic ' + str(base64.b64encode(plain_authorization.encode('utf-8')), 'utf-8')

    # http body
    body = None
    if method == 'POST' and post_parameters:
        body = urllib.parse.urlencode(string_to_dict(post_parameters, "=")).encode()

    # 处理重定向
    if not follow_redirection:
        # 禁止重定向
        opener = urllib.request.build_opener(NoHTTPRedirectHandler)
        urllib.request.install_opener(opener)

    # 设置超时
    default_socket_timeout_senonds = socket.getdefaulttimeout()
    socket.setdefaulttimeout(connect_timeout_seconds)

    try:
        response_page = ''

        # 请求
        real_url = urllib.request.quote(process_url(url), safe=";/?:@&=+$,")
        request_ = urllib.request.Request(url=real_url, headers=headers, data=body, method=method)
        response = urllib.request.urlopen(request_)

        #获取响应消息的协议头、网页（需解码）和状态码
        response_page = response.read()

        # 保存到本地文件
        if return_data_save_way == "save_to_disk":
            save_full_path = ""
            if file_save_way == "specify_folder":
                save_full_path = folder_save_path + "\\" + get_http_file_name(response, url)
            elif file_save_way == "specify_full_path":
                save_full_path = file_save_path

            save_to_file(save_full_path, response_page)

    except BaseException as e:
        raise ValueError('HTTP 出错')
    finally:
        # 恢复默认超时
        socket.setdefaulttimeout(default_socket_timeout_senonds)

    return response_page

class HttpResponse(object):
    def __init__(self, status_code, headers, body):
        self.status_code = status_code
        self.headers = headers
        self.body = body