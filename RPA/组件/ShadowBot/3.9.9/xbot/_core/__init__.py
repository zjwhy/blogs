import base64
import inspect
import os

_sdmodules = {}

def try_get_sdmodule():
    for stack in inspect.stack():
        folder = os.path.dirname(stack.filename)
        sdmodule = _sdmodules.get(folder, None)
        if sdmodule is not None:
            return sdmodule
    return None

def debug_print(base, *keys):
    def base64encode(value, format_str=False):
        if format_str and isinstance(value, str):
            bvalue = f'\'{str(value)}\''.encode()
        else:
            bvalue = str(value).encode()
        return base64.b64encode(bvalue).decode()

    def dirvalue(value):
        if isinstance(value, dict):
            bdict = {}
            for key, value in value.items():
                if key == 'xbot' or key == 'xbot_visual':
                    continue
                bkey = base64encode(key)
                bvalue = base64encode(value, True)
                bdict[bkey] = bvalue
            return bdict
        else:
            propdict = {}
            for key in dir(value):
                propvalue = getattr(value, key)
                if not callable(propvalue):
                    propdict[key] = propvalue
            return debug_print(propdict)

    if base == 'package.variables':
        sdmodule = try_get_sdmodule()
        current = sdmodule['variables']
    else:
        current = base
    if len(keys) > 0:
        for key in keys:
            if isinstance(current, dict):
                current = current[key]
            else:
                current = getattr(current, key)
    return dirvalue(current)


def debug_set_value(base, value, *keys):
    if len(keys) == 0:
        return
    if base == 'package.variables':
        sdmodule = try_get_sdmodule()
        current = sdmodule['variables']
    else:
        current = base
    for key in keys[:-1]:
        if isinstance(current, dict):
            current = current[key]
        else:
            current = getattr(current, key)
    if isinstance(current, dict):
        current[keys[-1]] = value
    else:
        setattr(current, keys[-1], value)
