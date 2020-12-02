import os, shutil, fnmatch, ctypes, win32con, win32file
import win32com.client
import subprocess
import time
from win32 import win32gui
from functools import cmp_to_key
from ctypes import wintypes, windll
from ._core import visual_action
from xbot.app import logging
from xbot import win32
from xbot.win32 import clipboard

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
    功能：文件夹是否存在
    '''
    path = expand_path(args['path'])
    expect_exist = args['expect_exist'] == 'exist'

    is_dir = os.path.isdir(path)
    if expect_exist:
        return is_dir
    else:
        return not is_dir


@visual_action
def make(**args):    
    '''
    功能：创建文件夹，支持多级目录
    '''
    path = expand_path(args['path'])
    if not os.path.exists(path):
        os.makedirs(path)
    
    return os.path.exists(path)

@visual_action
def remove(**args):
    '''
    功能：删除文件夹
    '''
    path = expand_path(args['path'])
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)

def winsort(data):
    _StrCmpLogicalW = windll.Shlwapi.StrCmpLogicalW
    _StrCmpLogicalW.argtypes = [wintypes.LPWSTR, wintypes.LPWSTR]
    _StrCmpLogicalW.restype  = wintypes.INT

    cmp_fnc = lambda psz1, psz2: _StrCmpLogicalW(psz1, psz2)
    return sorted(data, key=cmp_to_key(cmp_fnc))

@visual_action
def find_files(**args):
    '''
    功能：查找文件列表
    '''
    path = expand_path(args['path'])
    patterns = args['patterns'].split(',')
    find_subdir = args['find_subdir']
    skip_hidden_file = args.get('skip_hidden_file', False)

    is_sort = args.get('is_sort', False)
    sort_by = args.get('sort_by', 'name')
    sort_way = args.get('sort_way', 'increase')

    result = []
    for root, dirs, files in os.walk(path):
        for file_name in files:
            for pattern in patterns:                
                if fnmatch.fnmatch(file_name, pattern):
                    file_path = os.path.join(root, file_name)
                    if not skip_hidden_file or not (win32file.GetFileAttributesW(file_path) & win32con.FILE_ATTRIBUTE_HIDDEN):
                        result.append(file_path)
                    break
        if not find_subdir:
            break

    if is_sort:
        reverse = (sort_way == 'decrease')

        if sort_by == 'name':
            result = winsort(result)
            if reverse:
                result.reverse()

        elif sort_by == 'size':
            result = sorted(result, key=lambda file_path: os.stat(file_path).st_size, reverse=reverse)

        elif sort_by == 'create_time':
            result = sorted(result, key=lambda file_path: os.stat(file_path).st_ctime, reverse=reverse)

        elif sort_by == 'last_modify_time':
            result = sorted(result, key=lambda file_path: os.stat(file_path).st_mtime, reverse=reverse)

        else:
            raise ValueError('排序因素取值不正确')
   
    return result

@visual_action
def find_subdirs(**args):
    '''
    功能：查找子文件夹
    '''
    path = expand_path(args['path'])
    patterns = args['patterns'].split(',')
    find_subdir = args['find_subdir']

    result = []
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            for pattern in patterns:                
                if fnmatch.fnmatch(dir_name, pattern):
                    result.append(os.path.join(root, dir_name))
                    break
        if not find_subdir:
            break
    return result

@visual_action
def open(**args):
    '''
    功能：查找子文件夹
    'folder_file_path': 'xxx'
    '''
    folder_file_path = expand_path(args['folder_file_path'])

    if os.path.isdir(folder_file_path): # 只打开文件夹
        subprocess.Popen('explorer {}'.format(folder_file_path))
    elif os.path.isfile(folder_file_path): # 打开文件夹并选中文件
        subprocess.Popen('explorer /select,{}'.format(folder_file_path))
    else:
        raise FileNotFoundError('指定路径不存在: ' + folder_file_path)

@visual_action
def selected_dirs_or_files(**args):
    '''
    功能：获取当前激活的文件夹中选中的文件、文件夹列表
    'file_type': all/file/folder
    '''
    file_type = args['file_type']

    cur_hwnd = win32gui.GetForegroundWindow()
    clsid='{9BA05972-F6A8-11CF-A442-00A0C90A8F39}' # ShellWindows
    shell_windows=win32com.client.Dispatch(clsid)
    
    result = []
    target_shells = []
    # 0.过滤 IE窗口、非激活文件资源管理器
    for i in range(shell_windows.Count):
        is_ie_window = False
        try:
            is_ie_window = shell_windows[i].Type is not None
        except:
            pass

        try:
            if not is_ie_window and cur_hwnd == shell_windows[i].HWND:
                target_shells.append(shell_windows[i])
        except IndexError: 
            # 遇到过一次 site-packages\win32com\client\dynamic.py但是没法重现 
            # self._get_good_object_(self._enum_.__getitem__(index))
            # raise IndexError("list index out of range")
            pass
    
    paths = []
    # 1.获取选中的所有 Paths
    if len(target_shells) == 0: # 获取桌面选中文件(夹)列表
        win32.send_keys('^{c}')
        paths = clipboard.get_file_path()
        clipboard.clear()
    else: # 获取文件资源管理器选中文件(夹)列表
        while target_shells[0].Busy: # 等待非忙状态
            time.sleep(0.1)
        if target_shells[0].Document:
            for j in range(target_shells[0].Document.SelectedItems().Count):
                value = target_shells[0].Document.SelectedItems().Item(j).Path
                paths.append(value)
        # if len(paths) == 0: # win32gui失败的情况下尝试使用剪切板获取
        #     paths = clipboard.get_file_path()
    
    # 2.根据 file_type对 Paths筛选
    for idx in range(len(paths)):
        path = paths[idx]
        if file_type == 'all':
            result.append(path)
        elif file_type == 'file' and os.path.isfile(path):
            result.append(path)
        elif file_type == 'folder' and os.path.isdir(path):
            result.append(path)        

    return result

@visual_action
def empty(**args):
    '''
    功能：清空目录
    '''
    path = expand_path(args['path'])

    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            shutil.rmtree(os.path.join(path, dir_name))
        for file_name in files:
            os.remove(os.path.join(path, file_name))

@visual_action
def copy(**args):
    '''
    功能：拷贝目录
    '''
    source_dir_path = expand_path(args['source_dir_path'])
    copyto_dir_path = expand_path(args['copyto_dir_path'])
    overwrite = (args['copy_way'] == 'overwrite')

    parent_dir_path, dir_name = os.path.split(source_dir_path)
    dest_dir_path = os.path.join(copyto_dir_path, dir_name)

    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    for root, dirs, files in os.walk(source_dir_path):
        for dir in dirs:
            source_dir_path = os.path.join(root, dir)
            dest_dir_path = os.path.join(copyto_dir_path, source_dir_path.lstrip(parent_dir_path))
            if not os.path.exists(dest_dir_path):
                os.makedirs(dest_dir_path)

        for file in files:
            source_file_path = os.path.join(root, file)
            dest_file_path = os.path.join(copyto_dir_path, source_file_path.lstrip(parent_dir_path))

            if not os.path.exists(dest_file_path) or overwrite:
                parent_dir_path1, file_name = os.path.split(dest_file_path)
                if not os.path.exists(parent_dir_path1):
                    os.makedirs(parent_dir_path1)
                shutil.copyfile(source_file_path, dest_file_path)

    return dest_dir_path

@visual_action
def move(**args):
    '''
    功能：移动目录
    '''
    source_dir_path = expand_path(args['source_dir_path'])
    moveto_dir_path = expand_path(args['moveto_dir_path'])

    parent_dir_path, dir_name = os.path.split(source_dir_path)
    dest_dir_path = os.path.join(moveto_dir_path, dir_name)
    if os.path.exists(dest_dir_path):
        raise RuntimeError(dest_dir_path + '已存在，不能移动')

    shutil.move(source_dir_path, moveto_dir_path)
    return dest_dir_path

@visual_action
def get_special_dir(**args):
    '''
    功能：获取系统目录
    '''
    special_dir_name = args['special_dir_name']
    
    special_dirs = {
        'DesktopDirectory'      :0x0010,
        'ApplicationData'       :0x001a,
        'CommonApplicationData' :0x0023,
        'LocalApplicationData'  :0x001c,
        'Cookies'               :0x0021,
        'Favorites'             :0x0006,
        'History'               :0x0022,
        'InternetCache'         :0x0020,
        'Programs'              :0x0002,
        'MyMusic'               :0x000d,
        'MyPictures'            :0x0027,
        'Recent'                :0x0008,
        'SendTo'                :0x0009,
        'StartMenu'             :0x000b,
        'Startup'               :0x0007,
        'System'                :0x0025,
        'Templates'             :0x0015,
        'Personal'              :0x0005,
        'ProgramFiles'          :0x0026,
        'CommonProgramFiles'    :0x002b,
        'Windows'               :0x0024
        }

    special_dir_path = ''

    if special_dir_name == "TEMP":
        special_dir_path = os.environ[special_dir_name]
    elif special_dir_name in special_dirs.keys():
        dir_path = ctypes.create_string_buffer(1024)
        windll.shell32.SHGetSpecialFolderPathA(None, dir_path, special_dirs[special_dir_name], 0)
        special_dir_path = dir_path.value.decode('mbcs')

    return special_dir_path

@visual_action
def rename(**args):
    '''
    功能：文件夹重命名
    '''
    dir_path = args['path']
    new_name = args['new_name']
    root_path, dir_name = os.path.split(dir_path)
    new_dir_path = os.path.join(root_path, new_name)
    shutil.move(dir_path, new_dir_path)
    return new_dir_path