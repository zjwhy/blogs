from ._core import visual_action, parseint_from_args, parsefloat_from_args
import typing
import re

@visual_action
def get_text_length(**args) -> int:
    """
    {
        'text':'',
        'get_byte_length':True/False
    }
    """

    text = args['text']
    return len(text)
    #get_byte_length = args['get_byte_length']

    #if get_byte_length == False:
        #return len(text)
    #else:
        #bytes_array = bytes(text, encoding='utf8')
        # len_utf8 = len(text.encode(encoding='utf8'))
        # bytes_length = (len_utf8 - len(text)) / 2 + len(text)
        # return int(bytes_length)


@visual_action
def append_text_in_newline(**args) -> str:
    """
        'text':'',
        'new_line_text':''
    """

    text = args['text']
    new_line = args['new_line']
    new_line_text = args['new_line_text']

    if new_line:
        new_text = f'{text}\r\n{new_line_text}'
    else:
        new_text = f'{text}{new_line_text}'

    return new_text


@visual_action
def sub_text(**args) -> str:
    """
        'text':'',
        'start_way':'begin/positon'
        'start_index':0,
        'sub_way':'end/length'
        'sub_length':1
    """

    # 1、预处理
    text = args['text']

    # 2、起始位置
    start_index = 0
    if args['start_way'] == 'positon':
        start_index = parseint_from_args(args, 'start_index')

    # 3、终止位置
    end_index = len(text) - 1
    if args['sub_way'] == 'length':
        sub_length = parseint_from_args(args, 'sub_length')
        end_index = start_index + sub_length - 1

    # 4、截取
    return text[start_index:end_index + 1]    # 前闭后开[)


@visual_action
def pad_text(**args) -> str:
    """
        'text':'',
        'pad_way':'left/right',
        'pad_text':'',
        'total_length':10,
    """
    
    # 1、预处理
    #'hello'.ljust(10,'123')
    text = args['text']
    pad_way = args['pad_way']
    pad_text = args['pad_text']
    total_length = parseint_from_args(args, 'total_length')

    # 2、计算待添加的字符串chars_to_pad
    num_of_chars_need_to_pad = total_length - len(text)
    chars_to_pad=''
    i=0
    while i < num_of_chars_need_to_pad:
        chars_to_pad = chars_to_pad + pad_text[ i % len(pad_text) ]
        i += 1

    # 3、用chars_to_pad补齐原始文本text
    if pad_way == 'left':
        return chars_to_pad + text
    else:
        return text + chars_to_pad


@visual_action
def trim_text(**args) -> str:
    """
        'text':'',
        'trim_way':''
    """

    text = args['text']
    trim_way = args['trim_way']

    if trim_way == 'left':
        return text.lstrip()
    elif trim_way == 'right':
        return text.rstrip()
    else:
        return text.strip()


@visual_action
def change_text_case(**args) -> str:
    """
        'text':'',
        'case_type':'upper/lower/title/sentence'
    """

    text = args['text']
    case_type = args['case_type']

    if case_type == 'upper':
        return text.upper()
    elif case_type == 'lower':
        return text.lower()
    else:
        return text.title()


@visual_action
def text_to_number(**args) -> int:
    """
        'text':''
    """

    return parseint_from_args(args, 'text')


@visual_action
def number_to_text(**args) -> str:
    """
        'num':123456.789,
        'float_places':2,
        'use_1000_separator':True
    """

    num = parsefloat_from_args(args, 'num')
    float_places = parseint_from_args(args, 'float_places')
    use_1000_separator = args['use_1000_separator']

    float_format = f'.{str(float_places)}f'
    separator_format = ',' if use_1000_separator == True else ''
    text_format = '{}{}{}{}'.format('{:',separator_format,float_format,'}')

    return text_format.format(num)


@visual_action
def join_list_to_text(**args) -> str:
    """
        'list_to_join':[]/()
        'delimiter_way':'no'/'standard'/'custom',
        'standard_delimiter':'space'/'tab'/'new_line',
        'num_standard_delimiter':1,
        'custom_delimiter':''
    """

    # 1、预处理
    list_to_join = args['list_to_join']
    delimiter_way = args['delimiter_way']

    # 2、计算分隔符
    join_chars = ''
    if delimiter_way == 'no':
        pass
    elif delimiter_way == 'custom':
        join_chars = args['custom_delimiter']
    else:
        standard_delimiter = args['standard_delimiter']
        num_standard_delimiter = parseint_from_args(args, 'num_standard_delimiter')
        map_obj = {'space':' ','tab':'\t','new_line':'\r\n'}
        for _ in range(num_standard_delimiter):
            join_chars += map_obj[standard_delimiter]

    # 3、分割列表
    list_to_join = [str(value) for value in list_to_join]
    return join_chars.join(list_to_join)


@visual_action
def split_text_to_list(**args) -> typing.List[str]:
    """
        'text_to_split':''
        'delimiter_way':'standard'/'custom',
        'standard_delimiter':'space'/'tab'/'new_line',
        'num_standard_delimiter':1,
        'custom_delimiter':'',
        'is_regular_expression':True/False,
        'remove_empty':True/False
    """

    # 1、预处理
    text_to_split = args['text_to_split']
    delimiter_way = args['delimiter_way']
    standard_delimiter = args['standard_delimiter']
    custom_delimiter = args['custom_delimiter']
    is_regular_expression = args.get('is_regular_expression', False)
    remove_empty = args.get('remove_empty', False)

    # 2、分割
    text_list = []
    if delimiter_way == 'custom':
        if is_regular_expression:
            text_list = re.split(custom_delimiter, text_to_split)
        else:
            text_list = text_to_split.split(custom_delimiter)
    else:
        if standard_delimiter == 'space':
            text_list = text_to_split.split(' ')
        elif standard_delimiter == 'tab':
            text_list = text_to_split.split('\t')
        elif standard_delimiter == 'new_line':
            text_list = re.split('\r\n|\r|\n', text_to_split)

    if remove_empty:
        while '' in text_list:
            text_list.remove('')

    return text_list

@visual_action
def extract_content_from_text(**args) -> typing.Any:
    """
        'text':'',
        'extract_way':'',
        'pattern':'',
        'just_get_first': True/False,
        'ignore_case': True/False
    """
    
    # 1、预处理
    text = args['text']
    #extract_way = args['extract_way']
    regular_pattern = args['regular_pattern']
    just_get_first = args['just_get_first']
    ignore_case = re.IGNORECASE if args['ignore_case'] == True else 0

    # 2、构造正则对象
    flags = 0 | ignore_case     #| re.ASCII
    reg_obj = re.compile(regular_pattern, flags)

    # 3、计算匹配结果
    result_list = []
    for match_item in reg_obj.finditer(text):
        if len(match_item.groups()) == 0:   #这里的groups()方法不包括整个串 (表示没有匹配的子串)
            result_list.append(match_item.group(0))     #这里的group(0)代表整个串
        else:
            result_list.append(match_item.group(1))     #取第一个子串

    # 4、returnVO
    if just_get_first == True:
        if len(result_list) == 0:   #没有匹配项
            return None
        else:
            return result_list[0]
    else:
        return result_list
        

@visual_action
def replace_content_from_text(**args)->str:
    text = args['text']
    replace_way = args['replace_way']
    regular_pattern = args['regular_pattern']
    just_get_first = args['just_get_first']
    repalce_text = args['replace_text']
    dest_text = args['dest_text']
    ignore_case = re.IGNORECASE if args['ignore_case'] == True else 0
    flags = 0 | ignore_case
    if replace_way == "content":
        if just_get_first:
            return text.replace(repalce_text, dest_text, 1)
        else:
            return text.replace(repalce_text, dest_text)
    else:
        reg_obj = re.compile(regular_pattern, flags)
        if just_get_first == True:
            return reg_obj.sub(dest_text, text, 1)
        else:
            return reg_obj.sub(dest_text, text)
  
