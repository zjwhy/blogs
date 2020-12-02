import os, subprocess, typing

def _get_zipexe_path():
    path = os.getcwd()
    return os.path.join(path, r'7za.exe')

def zip(file_folder_path, zip_file_path, *, compress_level=5, password=None) -> typing.NoReturn:
    '''
    压缩文件/文件夹
    * @param file_folder_path, 待压缩的文件和文件夹，例如："C:\\1.txt" "C:\\2.txt"
    * @param zip_file_path, 压缩文件路径
    * @param compress_level, 压缩级别，取值 1~9，默认5，数字越大压缩率越高
    * @param password, 密码
    '''
    if os.path.exists(zip_file_path):
        raise ValueError(f'{zip_file_path} 已经存在')

    zipexe_path = _get_zipexe_path()

    cmd = ''
    if password in ['', None]:
        cmd = f'{zipexe_path} a -tzip -mx{compress_level} -y "{zip_file_path}" {file_folder_path}'
    else:
        cmd = f'{zipexe_path} a -tzip -mx{compress_level} -p"{password}" -y "{zip_file_path}" {file_folder_path}'

    process_ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process_ret.returncode != 0:
        raise ValueError(f'文件压缩失败，7za.exe 退出代码：{process_ret.returncode}')


def unzip(zip_file_path, unzip_dir_path, *, password=None) -> typing.NoReturn:
    '''
    解压文件/文件夹
    * @param zip_file_path, 压缩文件路径
    * @unzip_dir_path，解压路径
    * @param password, 密码
    '''
    if not os.path.exists(zip_file_path):
        raise ValueError(f'{zip_file_path} 不存在！')

    zipexe_path = _get_zipexe_path()

    cmd = ''
    if password == '':
        cmd = f'{zipexe_path} x -o"{unzip_dir_path}" -y "{zip_file_path}"'
    else:
        cmd = f'{zipexe_path} x -p"{password}" -o"{unzip_dir_path}" -y "{zip_file_path}"'

    process_ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process_ret.returncode != 0:
        raise ValueError(f'文件解压失败，7za.exe 退出代码：{process_ret.returncode}')