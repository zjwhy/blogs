from ._core import visual_action, parseint_from_args

import typing
import numbers


@visual_action
def test(**args) -> bool:
    """
    {
        'operand1': <any>,
        'operator': 'in',
        'operand2': <any>,
    }
    """
    operator = args['operator']
    operand1 = args['operand1']
    operand2 = args['operand2']

    def is_number(value):
        return isinstance(value, numbers.Number) and not isinstance(value, bool)

    def try_parse_float(value):
        try:
            return float(value)
        except ValueError:
            return value

    # 如果是数字与字符串比较，则统一转换为数字类型进行比较（为了降低可视化门槛）
    if type(operand1) != type(operand2):
        if isinstance(operand1, str) and is_number(operand2):
            operand1 = try_parse_float(operand1)
        elif isinstance(operand2, str) and is_number(operand1):
            operand2 = try_parse_float(operand2)

    if operator == '==':
        return operand1 == operand2
    elif operator == '!=':
        return operand1 != operand2
    elif operator == '>':
        return operand1 > operand2
    elif operator == '>=':
        return operand1 >= operand2
    elif operator == '<':
        return operand1 < operand2
    elif operator == '<=':
        return operand1 <= operand2
    elif operator == 'in':
        return operand2 in operand1
    elif operator == 'not in':
        return operand2 not in operand1
    elif operator == 'is true':
        return operand1 == True
    elif operator == 'is false':
        return operand1 == False
    elif operator == 'is none':
        return operand1 is None
    elif operator == 'not none':
        return operand1 is not None
    elif operator == 'is empty':
        return operand1 == ''
    elif operator == 'not empty':
        return operand1 != ''
    elif operator == 'starts with':
        return operand1 and isinstance(operand1, str) and operand1.startswith(operand2)
    elif operator == 'not starts with':
        return not (operand1 and isinstance(operand1, str) and operand1.startswith(operand2))
    elif operator == 'ends with':
        return operand1 and isinstance(operand1, str) and operand1.endswith(operand2)
    elif operator == 'not ends with':
        return not (operand1 and isinstance(operand1, str) and operand1.endswith(operand2))
    else:
        return False


@visual_action
def range_iterator(**args) -> typing.Iterable:
    """
    {
        'start': 0,
        'stop': 10,
        'step': 1,
    }
    """
    start = parseint_from_args(args, 'start')
    step = parseint_from_args(args, 'step')
    stop = parseint_from_args(args, 'stop')
    if step > 0:
        return range(start, stop + 1, step)
    else:
        return range(start, stop - 1, step)


@visual_action
def list_iterator(**args) -> typing.List:
    """
    {
        "list": []
    }
    """
    return args['list']
