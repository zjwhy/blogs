from ._core import visual_action, parseint_from_args
from xbot._core.retry import Retry
from xbot.win32 import screenshot
from xbot.app import dialog

import os
import subprocess


@visual_action
def run_application(**args) -> tuple:
    """
    {
        'application_path':'',
        'command_line_arguments': '',
        'working_folder': '',
        'after_application_launch':'',
        'is_wait_not_more_than':'',
        'wait_time':''
    }
    """

    #1、预处理
    application_path = args['application_path']
    command_line_arguments = args['command_line_arguments']
    working_folder = args['working_folder'] if args['working_folder'] != '' else None   #
    after_application_launch = args['after_application_launch']
    is_wait_infinity = not args['is_wait_not_more_than']
    wait_time = 0
    if is_wait_infinity == False:
        wait_time = parseint_from_args(args, 'wait_time')

    #2、获取文件名和扩展名
    # filepath, tmpfilename = os.path.split(application_path)
    # shotname, extension = os.path.splitext(tmpfilename)
    extension = os.path.splitext( os.path.split(application_path)[1] )[1]

    #3、开始执行
    process = subprocess.Popen(f'{application_path} {command_line_arguments}', cwd=working_folder, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, startupinfo=subprocess.STARTUPINFO())
    pid = process.pid

    #3.1 异步
    if after_application_launch == 'continue':
        return (pid, -1)
    #3.2 同步等待
    else:
        if is_wait_infinity == True:
            #sout , serr = process.communicate()  # 阻塞，等待子进程返回结果
            wait_time = 60*60*24*365*10  #模拟无限等待

        for _ in Retry(wait_time, interval=2, ignore_exception=True):
            command_code = process.poll()   #检测子进程中的命令是否结束，而不是检测子进程是否结束
            if (command_code) == None :   # wait_time秒内，子进程未结束
                continue
            else:
                return (pid, command_code) # wait_time秒内, 子进程结束
        
        return (pid, -1)    # wait_time秒后，子进程仍未结果, None


@visual_action
def run_dos_command(**args) -> tuple:
    """
        'dos_command':'',
        'working_folder': ''
    """

    dos_command = args['dos_command']
    working_folder = args['working_folder'] if args['working_folder'] != '' else None   #

    completedProcess = subprocess.run(dos_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_folder, input=None, universal_newlines=True) #run方式是阻塞，等待子进程执行结束并返回结果
    return (completedProcess.stdout,completedProcess.stderr,completedProcess.returncode)


@visual_action
def terminal_process(**args):
    """
        'terminal_way': 'id/name'，
        'process_id': 8
        'process_name': 'xxx.exe'
    """

    if args['terminal_way'] == 'id':
        process_id = parseint_from_args(args, 'process_id')
        os.system(f'taskkill -f -t /pid {process_id}')  #/t 关闭cmd进程的同时关闭其所有的子进程(考虑打开文件的情况)

    else:
        process_name = args['process_name']
        os.system(f'taskkill -f -t /im {process_name}')

@visual_action
def take_screenshot(**args) -> bool:
    image_source = args['image_source']
    window = args['window']
    save_to = args['save_to']
    image_path = args['image_path']

    image_format = args.get('image_format', None)
    if save_to == 'file':
        if image_format is None:
            _, image_ext = os.path.splitext(image_path)
            image_ext = image_ext.lower()
            if image_ext in ['.bmp', '.dib'] :
                image_format = 'Bmp'
            elif image_ext in ['.jpg', '.jpeg', '.jpe', '.jfif'] :
                image_format = 'Jpeg'
            elif image_ext in ['.gif'] :
                image_format = 'Gif'
            elif image_ext in ['.tif', '.tiff'] :
                image_format = 'Tiff'
            elif image_ext in ['.png'] :
                image_format = 'Png'
        if image_format is None:
            raise ValueError('不能解析或者不支持文件的图片格式')

    if image_source == 'screen':
        if save_to == 'clipboard':
            screenshot.save_screen_to_clipboard()
        else:
            screenshot.save_screen_to_file(image_path, image_format)

    elif image_source == "window":
        if save_to == 'clipboard':
            screenshot.save_window_to_clipboard(window.hWnd)
        else:
            screenshot.save_window_to_file(window.hWnd, image_path, image_format)

    elif image_source == "foreground_window":
        if save_to == 'clipboard':
            screenshot.save_window_to_clipboard(0)
        else:
            screenshot.save_window_to_file(0, image_path, image_format)
    elif image_source == "dynamic_select":
        if save_to == 'clipboard':
            return screenshot.manual_to_clipboard()
        else:
            return screenshot.manual_to_file(image_path, image_format)