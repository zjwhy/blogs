# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.8 (tags/v3.6.8:3c6b436a57, Dec 24 2018, 00:16:47) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./antrobot.py
# Compiled at: 2021-05-18 22:09:51
# Size of source mod 2**32: 8486 bytes
"""
执行脚本
"""
import os, sys, psutil, traceback
from functools import wraps
from optparse import OptionGroup
from optparse import OptionParser
from com.huawei.antrobot.executor.os_executor import OsExecutor
from com.huawei.antrobot.utils import global_var
from com.huawei.antrobot.models.context import GLOBAL_CONTEXT
import com.huawei.antrobot.utils.join_path as join_path
from com.huawei.antrobot.utils.logger import Logger
from com.huawei.antrobot.utils.notification_displayer import DISPLAY_TIPS
from com.huawei.antrobot.utils.notification_displayer import SHOW_TIPS
from com.huawei.antrobot.utils.role_params_verification import AllowList
from com.huawei.antrobot.utils.utils import del_driver_process
from com.huawei.antrobot.utils.utils import get_robot_version
from com.huawei.antrobot.utils.utils import send_result_to_agent
from worker.listener_on_directory import ListenerOnDirectory
from worker.listener_on_websocket import ListenerOnWS
from worker.robot import Robot
from worker.robot_batch import RobotBatch
LISTENER_TYPE_PORT = 'listener_on_port'
LOGGER = Logger.get_logger(__name__)
CONSOLE_LOGGER = Logger.get_logger('console')

def main():
    parser = del_parser()
    options, _ = parser.parse_args()
    GLOBAL_CONTEXT.update_runtime_data({'options': options})
    if has_exclusive_options(options, parser):
        return
    run(options, parser)
    del_driver_process((psutil.Process(os.getpid())),
      all_process=(True if options.kill_process in ('True', 'true') else False))


def del_parser():
    parser = OptionParser()
    parser.add_option('-w', '--workdir', dest='work_dir', help='A standard robot project')
    parser.add_option('-b', '--batch', dest='batch', help='Run with an excel which multiple projects in')
    group = OptionGroup(parser, 'Specify each parameter of a project option', "Use these options when it's not a standard project directory.")
    group.add_option('-p', '--playbackfile', dest='playback_file', help='The path of the playback file')
    group.add_option('-d', '--datafile', dest='datafile', help='A optional input data dir')
    group.add_option('-o', '--output_dir', dest='output_path', help='Output directory')
    group.add_option('-i', '--img_dir', dest='img_path', help='A optional image directory')
    group.add_option('-s', '--start', dest='start', help='A optional start method')
    parser.add_option('-c', '--callback', dest='callback', help='start port, agent or studio')
    parser.add_option_group(group)
    group = OptionGroup(parser, 'Start Robot by listening option', 'Use these option if you want to start robot by listening mode.')
    group.add_option('-m', '--listen_mode', dest='listen_mode', help='listen mode:[listener_on_directory or listener_on_port]')
    group.add_option('-g', '--listen_target', dest='listen_target', help='path or port to be monitored')
    parser.add_option_group(group)
    group = OptionGroup(parser, 'Start bubble message prompt', 'Use these option if you want to start bubble message prompt.')
    group.add_option('-t', '--tips', dest='tips', action='store_true', help='notification display')
    group.add_option('-l', '--level', dest='level', help="notification level, must be in ['info', 'error', 'warning']")
    parser.add_option_group(group)
    parser.add_option('-k', '--kill', dest='kill_process', help='kil process')
    parser.add_option('-r', '--record_time', dest='record_time', action='store_true',
      help='record time consumption')
    return parser


def show_tip(func):

    @wraps(func)
    def inner(options, parser):
        if options.listen_mode:
            if not options.listen_target:
                SHOW_TIPS('Robot is starting')
                func(options, parser)
                SHOW_TIPS('Robot finished')
        else:
            func(options, parser)
        DISPLAY_TIPS.destroy()

    return inner


@show_tip
def run(options, parser):
    global CONSOLE_LOGGER
    if options.callback:
        GLOBAL_CONTEXT.update_runtime_data({'client_communication_port': options.callback})
    elif options.start:
        if options.start.lower() == 'online':
            AllowList(invoker='mc')
    elif options.start.lower() == 'studio':
        Logger.set_console_name('studio')
        CONSOLE_LOGGER = Logger.get_console_logger()
    else:
        CONSOLE_LOGGER.info(f"robot {get_robot_version()} started")
        if options.batch:
            RobotBatch(options.batch).run()
        else:
            if options.listen_mode:
                if options.listen_target:
                    if options.listen_mode == LISTENER_TYPE_PORT:
                        ListenerOnWS(options).run()
                else:
                    ListenerOnDirectory(options.listen_target).run()
            else:
                if options.work_dir or options.playback_file:
                    rbt = Robot(options)
                    rbt.run()
        parser.print_help()


def has_exclusive_options(options, parser_instance):
    """
    输入选项冲突检查
    :return:
    """
    if options.batch:
        if any([options.playback_file, options.datafile,
         options.output_path, options.img_path,
         options.work_dir, options.listen_mode]):
            parser_instance.error('option -b and [-p/-d/-o/-i/-w/-m] are mutually exclusive')
            return True
        elif options.listen_mode and any([options.playback_file, options.datafile,
         options.output_path, options.img_path,
         options.batch, options.work_dir]):
            parser_instance.error('option -m and [-p/-d/-o/-i/-w/-b] are mutually exclusive')
            return True
        if options.level:
            if options.level not in ('info', 'warning', 'error'):
                parser_instance.error("-l must be in ['info', 'error', 'warning']")
                return True
    else:
        if options.kill_process:
            if options.kill_process not in ('False', 'True', 'false', 'true'):
                parser_instance.error("-k must be in ['False', 'True']")
                return True
        if options.playback_file:
            options.output_path or parser_instance.error('-p must be used together with -o')
            return True


if __name__ == '__main__':
    try:
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
            main()
        except Exception as error:
            try:
                LOGGER.error(traceback.format_exc())
                CONSOLE_LOGGER.error(f"robot finished with exception, exception details: {error}")
            finally:
                error = None
                del error

        else:
            CONSOLE_LOGGER.info('robot finished')
    finally:
        LOG_FILE = join_path(global_var.get_save_workspace(), 'result.log')
        LOGGER.info('robot finished, begin backup run log')
        Logger.backup(LOG_FILE)
        LOGGER.info('robot finished, end backup run log')
        OsExecutor().run('release')