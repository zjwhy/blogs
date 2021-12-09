from xbot._core import os_sleep, uidriver, robot, pipe
import xbot
import xbot_visual

import importlib
import sys
import pdbx
import json
import codecs
import os

if sys.stdout.encoding is None or sys.stdout.encoding.upper() != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding is None or sys.stderr.encoding.upper() != 'UTF-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def main():
    robot_inputs = json.loads(input())

    os_sleep.start_prevent_os_sleep()

    robot.connect(robot_inputs['robot_pip'])
    uidriver.launch(robot_inputs['uia_pip'])

    if robot_inputs['environment_variables'] is not None:
        for env_key, env_value in robot_inputs['environment_variables'].items():
            os.environ[env_key] = env_value

    insert_index = sys.path.index(f'{os.getcwd()}\\python\\lib\\site-packages')
    for sys_path in reversed(robot_inputs['sys_path_list']):
        sys.path.insert(insert_index, sys_path)

    mod = importlib.import_module(robot_inputs['mod'])
    if robot_inputs['debug']:
        pdbx.set_trace()

    try:
        xbot.logging.info('开始执行...')
        mod.main({})
    finally:
        xbot.logging.info('执行结束!')


if __name__ == "__main__":
    main()
