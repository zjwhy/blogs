# -*- coding: utf-8 -*-
import zipfile as zf
import subprocess
import os
import shutil
import random
import string
from ubpa.encrypt import decrypt
from ubpa.ilog import ILog

__logger = ILog(__file__)


def zip_file(src_file, dst_file=None, pwd=None):
    '''
       :function: Compressed into ZIP format
       :param； src_file:the address of the local folder or file;
                         dst_file = r'D:\\xlss\\def\\ytu' or dst_file = r'D:\\xlss\\xlsss1.xlsx'
                dst_file: generate the absolute path of ZIP file;
                          src_file = r'D:\\abc\\abc.zip'
                pwd:add password when Compressed
        :return:
    '''

    __logger.debug('start compress the file or folder')

    try:
        if os.path.exists(src_file):
            cmd_7z = os.path.abspath(os.path.join(os.path.dirname(__file__),"../../../../")) + os.sep + "Com.Isearch.Func.AI" + os.sep + "7z.exe"

            temp_path = deal_folder(src_file)
            src_temp_path = temp_path + os.sep + "*"

            if dst_file != None:
                dst_temp_path = dst_file
            else:
                ''' compress to temp folder '''
                dst_temp_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../")) + os.sep + "temp"\
                                + os.sep + ''.join(random.sample(string.ascii_letters + string.digits, 8)) + ".zip"

            if pwd != None:

                p = subprocess.Popen(['zip', 'a', '-p' + decrypt(str(pwd)), dst_temp_path, src_temp_path], executable=cmd_7z)
                p.wait()
            else:
                p = subprocess.Popen(['zip', 'a', dst_temp_path, src_temp_path], executable=cmd_7z)
                p.wait()

            remove_folder_file(temp_path)

            __logger.debug('end compressing the file or folder')

            return dst_temp_path
        else:
            __logger.debug('file is not exist')
            return False
    except Exception as e:
        raise (e)


def unzip_file(src_file, dst_file, pwd=None):
    '''
     function:decompressed the ZIP file
      :param :src_file: the absolute address of local ZIP file ;
                        src_file = r'D:\\abc\\新建文abc.zip'
              dst_file:decompressed to the local folder;
                       dst_file = r'D:\\xlss\\aaaaa'
              pwd:the password when decompressing
      :return: the path after decompressing  or return False

    '''


    list_file = []
    __logger.debug('start uncompress the file or folder')
    try:
        if zf.is_zipfile(src_file):

            f = zf.ZipFile(src_file)
            for file in f.namelist():
                if pwd != None:
                    file_path = f.extract(file, dst_file, bytes(decrypt(str(pwd)), encoding='utf-8'))
                else:
                    file_path = f.extract(file, dst_file)

                if os.path.isfile(file_path):
                    list_file.append(file_path)

            f.close()
            __logger.debug('end uncompressing the file or folder')

            return list_file
        else:
            __logger.debug('file is not exist')
            return False
    except Exception as e:
        ''' e is RuntimeError class,ZipFile in line 1434  '''
        if "Bad password" in e.args[0]:
            __logger.debug('password is wrong')
        raise e


def deal_folder(src_file):
    try:
        temp_path = create_temp_folder()

        src_file_list = [file.strip().rstrip() for file in src_file.split(',')]
        for path in src_file_list:
            if os.path.isfile(path):
                '''file'''
                shutil.copy(path, temp_path)

            if os.path.isdir(path):
                '''folder'''
                copy_folder(path, temp_path)

        return temp_path
    except Exception as e:
        raise (e)

def copy_folder(src_file, des_file):

    try:
        folder_name = os.path.basename(src_file)
        os.chdir(des_file)
        os.mkdir(folder_name)
        des_file = des_file + os.sep + folder_name

        os.chdir(src_file)
        src_file = [os.path.join(src_file, file) for file in os.listdir()]
        for source in src_file:
            if os.path.isfile(source):
                ''' source:file，des_file:folder '''
                shutil.copy(source, des_file)
            if os.path.isdir(source):

                p, src_name = os.path.split(source)
                des_file = os.path.join(des_file, src_name)
                shutil.copytree(source, des_file)
    except Exception as e:
        raise (e)

def create_temp_folder():
    try:
        ran_folder_name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        temp_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../")) + os.sep + "temp"

        os.chdir(temp_path)
        os.mkdir(ran_folder_name)

        return temp_path + os.sep + ran_folder_name
    except Exception as e:
        raise (e)

def remove_folder_file(path):
    try:
        shutil.rmtree(path)
    except Exception as e:
        raise (e)














