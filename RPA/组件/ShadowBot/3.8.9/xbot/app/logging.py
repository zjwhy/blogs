'''
应用日志记录模块
'''


from xbot._core import robot


def debug(text):
    '''
    记录Debug(调试)日志信息
    * @param text, 需要记录的日志信息
    '''

    robot.execute(f'Log.Debug', {'text': str(text)})


def info(text):
    '''
    记录普通日志信息
    * @param text, 需要记录的日志信息
    '''

    robot.execute(f'Log.Info', {'text': str(text)})


def warning(text):
    '''
    记录警告日志信息
    * @param text, 需要记录的日志信息
    '''

    robot.execute(f'Log.Warning', {'text': str(text)})


def error(text):
    '''
    记录错误日志信息
    * @param text, 需要记录的日志信息
    '''

    robot.execute(f'Log.Error', {'text': str(text)})
