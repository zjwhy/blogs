from ._core import visual_action, parseint_from_args, parsefloat_from_args
from xbot import pdf

import os
import shlex
import time


@visual_action
def extract_text(**args):
    path = args['path']

    page_scope = args['page_scope']
    from_page = 1
    to_page = 1
    if page_scope == 'all':
        from_page = 1
        to_page = -1
    elif page_scope == 'single':
        from_page = parseint_from_args(args, 'page')
        to_page = parseint_from_args(args, 'page')
    elif page_scope == 'part':
        from_page = parseint_from_args(args, 'from_page')
        to_page = parseint_from_args(args, 'to_page')

    use_password = args['use_password']
    password = None
    if use_password:
        password = args['password']

    if not os.path.isfile(path):
        raise ValueError(f'{path}不是文件')

    return pdf.extract_text(path, from_page, to_page, password=password)


@visual_action
def extract_images(**args):
    path = args['path']

    page_scope = args['page_scope']
    from_page = 1
    to_page = 1
    if page_scope == 'all':
        from_page = 1
        to_page = -1
    elif page_scope == 'single':
        from_page = parseint_from_args(args, 'page')
        to_page = parseint_from_args(args, 'page')
    elif page_scope == 'part':
        from_page = parseint_from_args(args, 'from_page')
        to_page = parseint_from_args(args, 'to_page')

    name_prefix = args['name_prefix']
    save_to_dir = args['save_to_dir']
    use_password = args['use_password']
    password = None
    if use_password:
        password = args['password']

    if not os.path.isfile(path):
        raise ValueError(f'{path}不是文件')

    if not os.path.exists(save_to_dir):
        os.makedirs(save_to_dir)

    return pdf.extract_images(path, from_page, to_page, save_to_dir, password=password, name_prefix=name_prefix)


def get_save_to_path(save_to, save_way):
    if not os.path.exists(save_to):
        return save_to
    if save_way == "overwrite":
        return save_to
    elif save_way == "stop_extract_if_exist":
        return None
    elif save_way == "add_sequential_suffix":
        parts = os.path.splitext(save_to)
        for i in range(100):
            newpath = ''.join([parts[0], '_', str(
                round(time.time() * 1000)), str(i), parts[1]])
            if not os.path.exists(newpath):
                return newpath
        raise Exception('尝试自动添加文件后缀失败')


@visual_action
def extract_pages(**args):
    path = args['path']

    page_scope = args['page_scope']
    from_page = 1
    to_page = 1
    if page_scope == 'all':
        from_page = 1
        to_page = -1
    elif page_scope == 'single':
        from_page = parseint_from_args(args, 'page')
        to_page = parseint_from_args(args, 'page')
    elif page_scope == 'part':
        from_page = parseint_from_args(args, 'from_page')
        to_page = parseint_from_args(args, 'to_page')

    save_to = args['save_to']
    save_way = args['save_way']

    new_save_to = get_save_to_path(save_to, save_way)
    if new_save_to is None:
        return

    use_password = args['use_password']
    password = None
    if use_password:
        password = args['password']

    if not os.path.isfile(path):
        raise ValueError(f'{path}不是文件')

    return pdf.extract_pages(path, from_page, to_page, new_save_to, password=password)


@visual_action
def merge_pdfs(**args):
    path = args['paths']

    save_to = args['save_to']
    save_way = args['save_way']
    new_save_to = get_save_to_path(save_to, save_way)
    if new_save_to is None:
        return

    use_password = args['use_password']
    passwords = None
    if use_password:
        delimiter = args['delimiter']
        passwords = args['passwords'].split(delimiter)

    str = shlex.shlex(path, posix=True)
    str.whitespace = ' '
    str.whitesapce_split = True
    paths = list(str)

    for pathTmp in paths:
        if not os.path.isfile(pathTmp):
            raise ValueError(f'{pathTmp}不是文件')

    if use_password and len(passwords) != len(paths):
        raise ValueError("密码个数和文件个数不一样")

    return pdf.merge_pdfs(paths, new_save_to, passwords=passwords)
