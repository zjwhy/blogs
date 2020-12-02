'''
win32截图自动化模块
'''


from .._core import uidriver, robot

def save_screen_to_clipboard():
    '''
    截屏并将图片添加到剪切板
    '''

    uidriver.execute('ScreenShot.SaveScreenToClipboard', {})

def save_screen_to_file(image_path, image_format):
    '''
    截屏并将图片保存到本地
    * @param image_path, 截图保存完整路径, 如 c:\\123.jpg
    * @param image_format, 截图保存的文件格式, 如png、jpg等
    '''

    uidriver.execute('ScreenShot.SaveScreenToFile', {
            'imagePath' : image_path,
            'imageFormat' : image_format
        })

def save_window_to_clipboard(hwnd):
    '''
    对指定窗口截图并将图片添加到剪切板, 句柄为0则选择当前激活的窗口
    * @param hWnd, 目标窗口的句柄, 可通过窗口对象`xbot.win32.window.Win32Window`的hWnd属性获得
    '''

    uidriver.execute('ScreenShot.SaveWindowToClipboard', {
            'hWnd' : hwnd
        })

def save_window_to_file(hwnd, image_path, image_format):
    '''
    对指定窗口截图并将图片保存到本地
    * @param hWnd, 目标窗口的句柄, 可通过窗口对象`xbot.win32.window.Win32Window`的hWnd属性获得
    * @param image_path, 截图保存完整路径, 如 c:\\123.jpg
    * @param image_format, 截图保存的文件格式, 如png、jpg等
    '''

    uidriver.execute('ScreenShot.SaveWindowToFile', {
            'hWnd' : hwnd,
            'imagePath' : image_path,
            'imageFormat' : image_format
        })


def manual_to_file(image_path, image_format) -> bool:
    '''
    对运行中用户指定的动态区域截图，并保存为本地文件
    * @param image_path, 截图保存完整路径, 如 c:\\123.jpg
    * @param image_format, 截图保存的文件格式, 如png、jpg等
    '''
    return robot.execute(f'Dialog.ShowImageSpyOverlay', {
        'settings':{
            'save_to': 'file',
            'image_path': image_path, 
            'image_format': image_format
            }
        }
    )


def manual_to_clipboard() -> bool:
    '''
    对运行中用户指定的动态区域截图，并保存到剪贴板中
    '''
    return robot.execute(f'Dialog.ShowImageSpyOverlay', {
        'settings':{
            'save_to': 'clipboard'
            }
        }
    )