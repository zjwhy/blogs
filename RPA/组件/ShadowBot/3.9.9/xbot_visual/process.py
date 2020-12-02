from ._core import visual_action, _isalambda, dict_to_object
from xbot.app import storage
import importlib
import xbot


@visual_action
# def run(**args) -> None:
#     """
#     {
#         "process": 'process1'
#         "package": __name__
#     }
#     """
#     mod = importlib.import_module(f"..{args['process']}", args['package'])
#     mod.main(None)


@visual_action
def invoke_module(**args) -> None:
    """
    {
        "module": 'module1',
        "package": __name__,
        "function": 'function1',
        "params": {}
    }
    """
    mod = importlib.import_module(f"..{args['module']}", args['package'])
    function = args['function']
    kwargs = args['params']
    for key, value in kwargs.items():
        if _isalambda(value):
            kwargs[key] = value()  # calc lambda
        else:
            kwargs[key] = value
    return getattr(mod, function)(**kwargs)


@visual_action
def get_app_params(**args) -> any:
    param_name = args['param_name']
    return xbot.app.get_app_params(param_name)

@visual_action
def run(**args) -> tuple:
    """
    {
        "module": 'xbot_ext.xxccvv.module1',
        "inputs": {}, # {'key1': 'val1'}
        "outputs": [] # ['key2', 'key3']
    }
    """

    inputs = args.get('inputs', None)
    outputs = args.get('outputs', None)
    process = args['process']

    if outputs is not None:
        prargs = {}.fromkeys(outputs)
    else:
        prargs = None
    if inputs is not None:
        for key, value in inputs.items():
            if _isalambda(value):
                prargs[key] = value()
            else:
                prargs[key] = value

    #应用内流程调用与自定义指令区别：process只有名称、返回值需要封装
    invoke_activity = False
    if len(process.split('.')) > 1:
        module_name = process
        invoke_activity = True
    else:
        module_name =  f"..{process}"
    mod = importlib.import_module(f"{module_name}", args['package'])
    mod.main(prargs)
    if prargs is not None:
        if not invoke_activity:
            process = process.replace('.','_')
            return dict_to_object(f'InvokeProcessResult_Dynamic_{process}', prargs)
        else:

            results = [prargs.get(output,None) for output in outputs]
            if len(results) == 1:
                return results[0]
            else:
                return tuple(results)
    return None

@visual_action
def write_to_storage(**args):
    """
        'key':'',
        'content':''
    """
    key = args['key']
    content = args['content']
    storage.write(key, content)



@visual_action
def read_from_storage(**args) -> str:
    """
        'key':''
    """
    key = args['key']
    return storage.read(key)