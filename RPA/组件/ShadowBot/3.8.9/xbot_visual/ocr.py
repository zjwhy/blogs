import os, re

from ._core import visual_action,parseint_from_args,parsesudoku_from_args
from xbot._core.retry import Retry
from xbot import ai

@visual_action
def create_ai_engine(**args):
    engine = args['engine']
    param1 = args['param1']
    param2 = args['param2']

    if engine == 'baidu':
        return ai.BaiduAI(param1, param2, edition=args.get('baidu_ocr_edition'))
    elif engine == 'tencent':
        return ai.TencentAI(param1, param2, edition=args.get('tencent_ocr_edition'))
    elif engine == 'aliyun':
        return ai.AliyunAI(param1, edition=args.get('aliyun_ocr_edition'))


@visual_action
def ocr_to_text(**args):
    string_list = ocr_to_text_internal(args)
    return '\r\n'.join(string_list)


@visual_action
def hover_on_text(**args):
    image_source = args["image_source"]
    text_to_find = args["text"]

    sudoku_part = parsesudoku_from_args(args, 'sudoku_part')
    offset_x = parseint_from_args(args, 'offset_x')
    offset_y = parseint_from_args(args, 'offset_y')

    delay_after = parseint_from_args(args, 'delay_after', 0)
    occurrence = parseint_from_args(args, 'occurrence')

    if image_source == 'screen':
        args["ai_engine"].hover_on_text_in_screen(text_to_find, anchor=(sudoku_part, offset_x, offset_y), delay_after=delay_after, occurrence=occurrence)
    elif image_source == 'window':
        args["ai_engine"].hover_on_text_in_window(args["window"].hWnd, text_to_find, anchor=(sudoku_part, offset_x, offset_y), delay_after=delay_after, occurrence=occurrence)
    elif image_source == 'foreground_window':
        args["ai_engine"].hover_on_text_in_window(0, text_to_find, anchor=(sudoku_part, offset_x, offset_y), delay_after=delay_after, occurrence=occurrence)


@visual_action
def click_text(**args):
    image_source = args["image_source"]
    text_to_find = args["text"]

    sudoku_part = parsesudoku_from_args(args, 'sudoku_part')
    offset_x = parseint_from_args(args, 'offset_x')
    offset_y = parseint_from_args(args, 'offset_y')

    delay_after = parseint_from_args(args, 'delay_after', 0)
    occurrence = parseint_from_args(args, 'occurrence')

    clicks = args['clicks']
    keys = args.get('keys', 'none')
    keys = 'none' if keys == 'null' else keys
    move_mouse = args['move_mouse']

    if image_source == 'screen':
        args["ai_engine"].click_text_in_screen(text_to_find, button=args['button'], click_type=clicks, 
        anchor=(sudoku_part, offset_x, offset_y), delay_after=delay_after, move_mouse=move_mouse, occurrence=occurrence)
    elif image_source == 'window':
        args["ai_engine"].click_text_in_window(args["window"].hWnd, text_to_find, click_type=clicks, 
        anchor=(sudoku_part, offset_x, offset_y), delay_after=delay_after, move_mouse=move_mouse, occurrence=occurrence)
    elif image_source == 'foreground_window':
        args["ai_engine"].click_text_in_window(0, text_to_find, button=args['button'], click_type=clicks, 
        anchor=(sudoku_part, offset_x, offset_y), delay_after=delay_after, move_mouse=move_mouse, occurrence=occurrence)


@visual_action
def if_text_on_screen(**args):
    text         = args['text']
    is_regular_expression = args['is_regular_expression']
    desired_state= args['desired_state']

    exist = False
    string_list = ocr_to_text_internal(args)

    for string in string_list:
        if is_regular_expression:
            if re.match(text, string) != None:
                exist = True
                break
        else:
            if string.find(text) != -1:
                exist = True
                break

    return (exist and desired_state == 'exist') or (not exist and desired_state == 'not_exist')


@visual_action
def wait_text_on_screen(**args):
    text         = args['text']
    is_regular_expression = args['is_regular_expression']
    desired_state= args['desired_state']

    is_wait = args['is_wait']
    timeout_seconds = -1
    if is_wait:
        timeout_seconds = parseint_from_args(args, 'timeout_seconds')

    for _ in Retry(timeout_seconds, interval=2, ignore_exception=True):
        exist = False
        string_list = ocr_to_text_internal(args)

        for string in string_list:
            if is_regular_expression:
                if re.match(text, string) != None:
                    exist = True
                    break
            else:
                if string.find(text) != -1:
                    exist = True
                    break

        if (exist and desired_state == 'appear') or (not exist and desired_state == 'disappear'):
            return True

    return False


def ocr_to_text_internal(args):
    ai_engine    = args["ai_engine"]
    window       = args["window"]
    image_source = args["image_source"]
    image_path   = args.get("image_path", "")
    image_region = args["image_region"]

    if image_region == 'sub_region':
        region_x1    = parseint_from_args(args, "region_x1")
        region_y1    = parseint_from_args(args, "region_y1")
        region_x2    = parseint_from_args(args, "region_x2")
        region_y2    = parseint_from_args(args, "region_y2")

    string_list = []
        
    if image_source == 'screen':
        if image_region == 'all_region':
            string_list = ai_engine.ocr_from_screen()
        else:
            string_list = ai_engine.ocr_from_screen((region_x1, region_y1, region_x2, region_y2))

    elif image_source == 'window':
        if image_region == 'all_region':
            string_list = ai_engine.ocr_from_window(window.hWnd)
        else:
            string_list = ai_engine.ocr_from_window(window.hWnd, (region_x1, region_y1, region_x2, region_y2))

    elif image_source == 'foreground_window':
        if image_region == 'all_region':
            string_list = ai_engine.ocr_from_window(0)
        else:
            string_list = ai_engine.ocr_from_window(0, (region_x1, region_y1, region_x2, region_y2))

    elif image_source == 'image_on_disk':
        if not os.path.isfile(image_path):
            raise ValueError(f'文件（{image_path}）不存在')
        string_list = ai_engine.ocr_from_file(image_path)

    elif image_source == 'clipboard_image':
        string_list = ai_engine.ocr_from_clipboard_image()

    if string_list == None:
        return []
    else:
        return string_list