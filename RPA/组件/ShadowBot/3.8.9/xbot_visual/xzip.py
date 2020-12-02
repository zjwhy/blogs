import os, subprocess
from ._core import visual_action, parseint_from_args
import xbot


@visual_action
def zip(**args):
    file_folder_path = args['file_folder_path']
    password = args['password']
    compress_level = parseint_from_args(args, 'compress_level', 5)
    zip_file_path = args['zip_file_path']
    
    xbot.xzip.zip(file_folder_path, zip_file_path, compress_level=compress_level, password=password)

@visual_action
def unzip(**args):
    zip_file_path = args['zip_file_path']
    password = args['password']
    unzip_dir_path = args['unzip_dir_path']

    xbot.xzip.unzip(zip_file_path, unzip_dir_path, password=password)