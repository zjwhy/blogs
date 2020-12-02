from ._core import visual_action, parseint_from_args
from xbot._core.validation import valid, valid_multi, ValidPattern

@visual_action
def create(**args):
    return dict()


@visual_action
def set(**args):
    dictionary = args['dict']
    key = args['key']
    value = args['value']

    valid_multi('字典', dictionary, (ValidPattern.NotNone, (ValidPattern.Type, dict)))

    dictionary[key] = value

@visual_action
def get_value(**args):
    dictionary = args['dict']
    key = args['key']
    process_way = args.get('key_not_exist_process_way', 'raise_error')
    default_value = args.get('default_value', None)

    valid_multi('字典', dictionary, (ValidPattern.NotNone, (ValidPattern.Type, dict)))

    if key not in dictionary:
        if process_way == 'raise_error':
            raise ValueError(f'字典不存在 {key} 这个key')
        elif process_way == 'return_default_value':
            return default_value
        else:
            raise ValueError(f'"键不存在时"参数取值错误！')
    else:
        return dictionary[key]


@visual_action
def get_keys(**args):
    dictionary = args['dict']

    valid_multi('字典', dictionary, (ValidPattern.NotNone, (ValidPattern.Type, dict)))

    return list(dictionary.keys())


@visual_action
def get_values(**args):
    dictionary = args['dict']

    valid_multi('字典', dictionary, (ValidPattern.NotNone, (ValidPattern.Type, dict)))

    return list(dictionary.values())


@visual_action
def pop(**args):
    dictionary = args['dict']
    key = args['key']

    valid_multi('字典', dictionary, (ValidPattern.NotNone, (ValidPattern.Type, dict)))

    try:
        dictionary.pop(key)
    except:
        pass