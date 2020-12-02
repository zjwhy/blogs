from .._core import visual_action, parseint_from_args, parsefloat_from_args
from xbot.app import logging
from . import databook

import time
import typing
import random


@visual_action
def log(**args):
    """
    {
        'type': 'info',
        'text': <any>,
    }
    """
    log_type = args['type']
    if log_type == 'info':
        logging.info(args['text'])
    elif log_type == 'debug':
        logging.debug(args['text'])
    elif log_type == 'warning':
        logging.warning(args['text'])
    elif log_type == 'error':
        logging.error(args['text'])
    else:
        pass


@visual_action
def sleep(**args):
    """
    {
        'seconds': 1
    }
    """
    secs = parsefloat_from_args(args, 'seconds')
    time.sleep(secs)


@visual_action
def variable(**args) -> typing.Any:
    """
    {
        'value': 1
    }
    """
    return args['value']

@visual_action
def random_int(**args) -> typing.Any:
    """
    {
        'start_number': 1
        'stop_number': 1
    }
    """
    start_number = parseint_from_args(args, 'start_number')
    stop_number = parseint_from_args(args, 'stop_number')

    if start_number > stop_number:
        raise ValueError(f'当前最小数（{start_number}）大于最大数（{stop_number}）')

    return random.randint(start_number, stop_number)