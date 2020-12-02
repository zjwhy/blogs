# -*- coding: utf-8 -*-

from ubpa.ilog import ILog
import shutil
import glob
import os
import time
import fnmatch
import chardet
__logger = ILog(__file__)


def create_file(file=None, path=None):
    '''
    创建文件
    :param file:文件名称
    :param path:文件路径
    '''
    __logger.echo_msg(u"ready to execute[create_file]")
    try:
        file = open(path + os.sep + file, 'w')
        file.close()
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[create_file]")


def create_dir(dir=None):
    '''
    创建路径
    :param dir:文件路径
    '''
    __logger.echo_msg(u"ready to execute[create_dir]")
    try:
        os.makedirs(dir)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[create_dir]")


def copy_file(src_file=None,dst_file=None):
    '''
    复制文件
    :param src_file:文件路径
    :param dst_file:存放路径
    '''
    __logger.echo_msg(u"ready to execute[copy_file]")
    try:
        shutil.copy(src_file, dst_file)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[copy_file]")


def del_file(file=None):
    '''
    删除文件
    :param file:文件路径
    '''
    __logger.echo_msg(u"ready to execute[del_file]")
    try:
        os.remove(file)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[del_file]")


def move_file(src_file=None, dst_file=None):
    '''
    移动文件
    :param src_file:  a file or directory
    :param dst_file:  a file or directory
    '''
    __logger.echo_msg(u"ready to execute[move_file]")
    try:
        shutil.move(src_file, dst_file)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[move_file]")


def filter_exclude_file(files,exclude_file):
    '''
    过滤不需要的文件
    '''
    dst_files = []
    try:
        if exclude_file != None:
            for f in files:
                a = f.split("/")
                if not fnmatch.fnmatch(a[-1], exclude_file):
                    dst_files.append(f)
            return dst_files
        else:
            return files
    except Exception as e:
        raise e


def get_all_path_files(path, include_file, sub_dir):
    '''
    满足条件的所有文件
    '''
    list_files=[]
    try:
        if sub_dir:
            path = os.path.join(path, '**')
            files = glob.glob(os.path.join(path, include_file), recursive=True)
            for i in files:
                i=i.replace('\\', '/')
                list_files.append(i)
        else:
            files = glob.glob(os.path.join(path, include_file), recursive=False)
            for i in files:
                i=i.replace('\\', '/')
                list_files.append(i)
        return list_files
    except Exception as e:
        raise e


def sort_by_time_reversed(files, reverse=True):
    '''
    时间排序
    '''
    return sorted(files, key=lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(x))),
                  reverse=reverse)


def find_files(path=None, include_file='*', exclude_file=None, sub_dir=False, time_sort='Desc', topn=50):
    '''
    通过指定文件名找到其所在路径
    参数:
        path: 需要检索的目录路径
        include_file: 需要检索的文件名
        exclude_file: 不需要检索的文件名
        sub_dir: 是否检索子文件夹
        time_sort: 按照时间排序
        topn: 前多少条
    return: 返回需要检索的文件路径列表
    '''
    __logger.echo_msg(u"ready to execute[find_files]")
    try:
        files = get_all_path_files(path, include_file, sub_dir)
        if time_sort == 'Desc':
            files = sort_by_time_reversed(files, reverse=True)
        else:
            files = sort_by_time_reversed(files, reverse=False)
        files = filter_exclude_file(files,exclude_file)
        files = files[0:topn]
        __logger.echo_msg(u"find_files result:" + str(files))
        return files
    except Exception as e:
        raise e


def read_file(filename=None, encoding=None):
    '''
        read_file(filename=None, encoding=None) -> str
            function：Read file
            parameter：
              filename : file path
              encoding : file encoding
                         The default is None, which is automatically recognized.
            return:
              str
            instance:
            read_file(filename="C:\\test.txt")  -> "IRPA read_file"
            read_file(filename="C:\\test.txt",encoding='utf-8')  -> "IRPA read_file"
    '''
    __logger.echo_msg(u"ready to execute[read_file]")
    try:
        if encoding == None:
            f = open(filename, 'rb')
            data = f.read()

            chardet_dict = chardet.detect(data)
            encoding_mode = chardet_dict['encoding']  # 获取文件的编码格式
            content = data.decode(encoding_mode)
            f.close()
        else:
            with open(filename, 'r', encoding=encoding) as f:
                content = f.read()
        return content
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[read_file]")


def write_file(filename=None, content=None, mode='a'):
    '''
        write_file(filename=None, content=None, mode='a')
            function：Write file
            parameter：
              filename : file path
              content  : What to write
              mode     : Write mode  The default is 'a' append mode
                                     Can be set to 'w'  overwrite write
            instance:
            write_file(filename="C:\\test.txt", content='test', mode='a')
            write_file(filename="C:\\test2.txt", content='test2', mode='w')
    '''
    __logger.echo_msg(u"ready to execute[write_file]")
    try:
        if mode == 'w':
            with open(file=filename, mode='w') as f:
                f.write(content)
        else:
            with open(file=filename, mode='a') as f:
                f.write(content)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[write_file]")


def get_file_size(filename=None):
    '''
            get_file_size(filename=None) -> int
                function：Get the file size in bytes
                parameter：
                  filename : file path
                return:
                  the file size
                instance:
                get_file_size(filename="C:\\test.txt")  -> 48
    '''
    __logger.echo_msg(u"ready to execute[get_file_size]")
    try:
        fsize = os.path.getsize(filename=filename)
        return fsize
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[get_file_size]")


def rename_file(src=None, dst=None):
    '''
            rename_file(src=None, dst=None)
                function：Rename file
                parameter：
                  src : Original file path
                  dst : Renamed file path
                instance:
                rename_file(src="C:\\test.txt", dst="C:\\new_test.txt")
    '''
    __logger.echo_msg(u"ready to execute[rename_file]")
    try:
        os.rename(src, dst)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[rename_file]")


def exist_file(filename=None):
    '''
            exist_file(filename=None) 
                function：Determine if the file exists
                parameter：
                  filename : file path
                return:
                  True  /  False
                instance:
                exist_file(filename="C:\\test.txt")  -> True or False
    '''
    __logger.echo_msg(u"ready to execute[exist_file]")
    try:
         return os.path.exists(path=filename)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[exist_file]")


def exist_dir(dir=None):
    '''
            exist_dir(dir=None)
                function：Determine if the Directory path exists
                parameter：
                  filename : Directory path
                return:
                  True  /  False
                instance:
                exist_dir(dir="C:\\Desktop")  -> True or False
    '''
    __logger.echo_msg(u"ready to execute[exist_dir]")
    try:
        return os.path.exists(dir)
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[exist_dir]")

