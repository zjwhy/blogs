import os, sys, shutil, ctypes, time
from os import path


from ._core import visual_action,parseint_from_args
from xbot.app import logging

def expand_path(path):
    '''
    功能：将path中的环境变量替换成实际路径
    '''
    ret_path = ctypes.create_unicode_buffer(1024)
    ctypes.windll.Kernel32.ExpandEnvironmentStringsW(path, ret_path, 1024)
    return ret_path.value

@visual_action
def if_exist(**args):
    '''
    功能：文件是否存在
    '''
    path = expand_path(args['path'])
    expect_exist = args['expect_exist'] == 'exist'

    is_file = os.path.isfile(path)
    if expect_exist:
        return is_file
    else:
        return not is_file

@visual_action
def remove(**args):
    '''
    功能：删除文件
    '''
    paths = args['paths']

    if isinstance(paths, str):
        temp_path = expand_path(paths)
        if os.path.isfile(temp_path):
            os.remove(temp_path)
    elif isinstance(paths, list):
        for path in paths:
            temp_path = expand_path(path)
            if os.path.isfile(temp_path):
                os.remove(temp_path)
    else:
        raise RuntimeError("路径类型不正确")

def read_bin(path):
    '''
    功能：读取二进制数据
    '''
    bin = None
    with open(path, 'rb') as f:
        bin = f.read()
        f.close()
    return bin

def read_text(path, encoding):
    '''
    功能：读取整个文本
    '''
    text = None
    with open(path, mode='r', encoding=encoding) as f:
        text = f.read()
        f.close()
    return text

def read_lines(path, encoding):
    '''
    功能：读取文本所有行
    '''
    lines = None
    with open(path, mode='r', encoding=encoding) as f:
        lines = f.readlines()
        f.close()
    return lines

@visual_action
def read(**args):
    '''
    功能：读文件
    '''
    path = expand_path(args['path'])
    read_way = args['read_way']
    encoding = args['encoding']
    if encoding == 'default':
        encoding = sys.getdefaultencoding()

    if read_way == 'bin':
        return read_bin(path)
    elif read_way == 'all_text':
        return read_text(path, encoding)
    elif read_way == 'lines':
        return read_lines(path, encoding)
    else:
        raise ValueError('读取方式参数取值不正确')

def write_bin(path, mode, bin):
    '''
    功能：写入二进制数据
    '''
    with open(path, mode=mode) as f:
        f.write(bin)
        f.close()    

def write_text(path, mode, encoding, text):
    '''
    功能：写入文本
    '''
    with open(path, mode=mode, encoding=encoding) as f:
        f.write(text)
        f.close()

@visual_action
def write(**args):
    '''
    功能：写文件
    '''
    path = expand_path(args['path'])
    content = args['content']
    append = (args['write_way'] == 'append')
    is_text = args['is_text']
    encoding = args['encoding']
    if encoding == 'default':
        encoding = sys.getdefaultencoding()

    mode = ''
    if is_text:
        if append:
            mode = 'a'            
        else:
            mode = 'w'
        #python在写入文本时，会将 \n 替换成 \r\n，这里先替换，以达到正常效果
        content = content.replace("\r\n", "\n")
        write_text(path, mode, encoding, content)
    else:
        if append:
            mode = 'ba'
        else:
            mode = 'bw'
        write_bin(path, mode, content.encode())

def copy_internal(source_file_path, copyto_dir_path, overwrite):
    source_dir_path, source_file_name = os.path.split(source_file_path)
    dest_file_path = os.path.join(copyto_dir_path, source_file_name)

    if not os.path.exists(dest_file_path) or overwrite:
        shutil.copyfile(source_file_path, dest_file_path)
        return dest_file_path

@visual_action
def copy(**args):
    '''
    功能：拷贝文件
    '''
    source_file_paths = args['source_file_paths']
    copyto_dir_path = expand_path(args['copyto_dir_path'])
    overwrite = (args['copy_way'] == 'overwrite')

    copyed_file_paths = []
    if isinstance(source_file_paths, str):
        copyed_file_path = copy_internal(expand_path(source_file_paths), copyto_dir_path, overwrite)
        if copyed_file_path != None:
            copyed_file_paths.append(copyed_file_path)
    elif  isinstance(source_file_paths, list):
        for source_file_path in source_file_paths:
            copyed_file_path = copy_internal(expand_path(source_file_path), copyto_dir_path, overwrite)
            if copyed_file_path != None:
                copyed_file_paths.append(copyed_file_path)
    else:
        raise ValueError('文件路径参数类型不正确')

    return copyed_file_paths

def move_internal(source_file_path, moveto_dir_path, overwrite):
    source_dir_path, source_file_name = os.path.split(source_file_path)
    dest_file_path = os.path.join(moveto_dir_path, source_file_name)

    if not os.path.exists(dest_file_path) or overwrite:
        shutil.move(source_file_path, dest_file_path)
        return dest_file_path

@visual_action
def move(**args):
    '''
    功能：移动文件
    '''
    source_file_paths = args['source_file_paths']
    moveto_dir_path = expand_path(args['moveto_dir_path'])
    overwrite = (args['move_way'] == 'overwrite')

    moved_file_paths = []

    if isinstance(source_file_paths, str):
        moved_file_path = move_internal(expand_path(source_file_paths), moveto_dir_path, overwrite)
        if moved_file_path != None:
            moved_file_paths.append(moved_file_path)
    elif  isinstance(source_file_paths, list):
        for source_file_path in source_file_paths:
            moved_file_path = move_internal(expand_path(source_file_path), moveto_dir_path, overwrite)
            if moved_file_path != None:
                moved_file_paths.append(moved_file_path)
    else:
        raise ValueError('文件路径参数类型不正确')

    return moved_file_paths

class FileParts(object):
    def __init__(self, drive_name, directory, file_name, file_name_without_extension, file_extension):
        self.drive_name = drive_name
        self.directory = directory
        self.file_name = file_name
        self.file_name_without_extension = file_name_without_extension
        self.file_extension = file_extension

@visual_action
def get_file_parts(**args):
    '''
    功能：获取文件路径信息
    '''
    file_path = args['path']

    root_dir, tmp = os.path.splitdrive(file_path)
    dir_path, file_name = os.path.split(file_path)
    file_name_no_extension, file_extension = os.path.splitext(file_name)

    return FileParts(root_dir, dir_path, file_name, file_name_no_extension, file_extension)

@visual_action
def wait(**args):
    '''
    功能：等待文件创建或者删除
    '''
    file_path = args['path']
    desired_state = args['desired_state']
    is_wait = args['is_wait']
    if is_wait:
        timeout_seconds = parseint_from_args(args, 'timeout_seconds')

    retry_times = timeout_seconds if is_wait else sys.maxsize
    result = False

    for i in range(retry_times):
        if desired_state == 'created':
            if os.path.isfile(file_path):
                result = True
                break
        elif desired_state == 'deleted':
            if not os.path.isfile(file_path):
                result = True
                break
        else:
            raise ValueError('参数取值不对')
        time.sleep(1)

    return result

@visual_action
def rename(**args):
    '''
    功能：文件重命名
    '''
    file_path = args['path']
    new_name = args['new_name']
    dir_path, file_name = os.path.split(file_path)
    new_file_path = os.path.join(dir_path, new_name)
    shutil.move(file_path, new_file_path)
    return new_file_path