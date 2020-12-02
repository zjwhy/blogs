import base64

from ._core import visual_action

@visual_action
def encode(**args):
    source = args['source']
    output_string = args['output_string']

    if not isinstance(source, (str, bytes)):
        raise ValueError('内容参数类型不正确')

    source_bytes = None
    if isinstance(source, str):
        source_bytes = source.encode('utf-8')
    else:
        source_bytes = source

    result = base64.b64encode(source_bytes)
    if output_string:
        return result.decode('utf-8')
    else:
        return result

@visual_action
def decode(**args):
    source = args['source']
    output_string = args['output_string']

    if not isinstance(source, (str, bytes)):
        raise ValueError('内容参数类型不正确')

    source_bytes = None
    if isinstance(source, str):
        source_bytes = source.encode('utf-8')
    else:
        source_bytes = source

    result = base64.b64decode(source_bytes)
    if output_string:
        return result.decode('utf-8')
    else:
        return result