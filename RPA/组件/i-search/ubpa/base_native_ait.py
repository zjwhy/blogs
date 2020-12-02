# -*- coding: utf-8 -*-
import os, re
import sys
import subprocess
from pkgutil import find_loader
import tempfile
import shlex
from glob import iglob
import random
import string

#AutoIt3.exe存放目录
autoit_cmd = os.path.abspath(os.path.join(os.path.dirname(__file__),"../../../"))+"\Com.Isearch.Func.AutoIt\AutoIt3.exe" 
def run_autoit(au3, agrs=None, nice=0): #au3 表示XXX.au3可执行文件
    try:
        command = []
        if not sys.platform.startswith('win32') and nice != 0:
            command += ('nice', '-n', str(nice))

        command += (autoit_cmd, au3)

        if agrs:
            for agr in agrs:
                command += (' ', agr)

        proc = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        status_code, error_string, stdout_string = proc.wait(), proc.stderr.read(), proc.stdout.read()

        proc.stderr.close()
        return status_code, error_string, stdout_string

    except Exception as e:
        raise e

def get_cmd_message(msg_string):
    return u' '.join(
        line for line in msg_string.decode('utf-8').splitlines()
    ).strip()
    
def get_cmd_message1(msg_string):
    return u' '.join(
        line for line in msg_string.decode('gbk').splitlines()
    ).strip()    

def set_au3_file_res_path(pfile):
    img_res_path = os.path.abspath(os.path.join(os.path.dirname(pfile), "../../../.."));
    return img_res_path

def gen_au3_file(params):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    au3_file_res_path = set_au3_file_res_path(__file__)
    au3_file_name = au3_file_res_path + "\\temp\\" + ran_str + ".au3"
    try:
        au3_file = open(au3_file_name, 'w',encoding="utf-8")
        au3_file.write(params)
    finally:
        if au3_file:
            au3_file.close()
        return au3_file_name


def cleanup(temp_name):
    ''' Tries to remove files by filename wildcard path. '''
    for filename in iglob(temp_name + '*'):
        try:
            os.remove(filename)
        except OSError:
            pass

