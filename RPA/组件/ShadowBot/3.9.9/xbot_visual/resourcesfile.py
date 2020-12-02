import os, ctypes
from ._core import visual_action, _expand_path
from xbot._core import try_get_sdmodule

@visual_action
def read(**args):
    sdmodule = try_get_sdmodule()
    resources = sdmodule['resources']

    file_name = args['file_name']
    read_way = args['read_way']
    encoding = args['encoding']

    if read_way == 'text':
        return resources.get_text(file_name, encoding)
    else:
        return resources.get_bytes(file_name)

@visual_action
def copy_to(**args):
    sdmodule = try_get_sdmodule()
    resources = sdmodule['resources']

    file_name = args['file_name']
    dest_file_name = args['dest_file_name']

    resources.copy_to(file_name, dest_file_name)

@visual_action
def copy_to_clipboard(**args):
    sdmodule = try_get_sdmodule()
    resources = sdmodule['resources']

    file_name = args['file_name']
    resources.copy_to_clipboard([_expand_path(file_name)])



    