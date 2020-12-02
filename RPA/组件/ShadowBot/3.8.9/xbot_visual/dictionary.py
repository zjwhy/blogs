from ._core import visual_action, parseint_from_args

@visual_action
def create(**args):
    return dict()


@visual_action
def set(**args):
    dict = args['dict']
    key = args['key']
    value = args['value']

    dict[key] = value

@visual_action
def get_value(**args):
    dict = args['dict']
    key = args['key']

    if key not in dict:
        raise ValueError(f'字典不存在 {key} 这个key')
    return dict[key]


@visual_action
def get_keys(**args):
    dict = args['dict']
    return list(dict.keys())


@visual_action
def get_values(**args):
    dict = args['dict']
    return list(dict.values())


@visual_action
def pop(**args):
    dict = args['dict']
    key = args['key']
    return dict.pop(key)