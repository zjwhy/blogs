'''
应用执行进度反馈模块
'''


from xbot._core import robot


def set_message(message):
    robot.execute(f'Progress.SetMessage', {'message': message})


def set_progress(value):
    robot.execute(f'Progress.SetProgress', {'value': value})
