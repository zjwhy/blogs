from ._core import visual_action

import json

@visual_action
def to_json(**args):
    text = args['text']
    return json.loads(text)

@visual_action
def to_text(**args) -> str:
    json_obj = args['json_obj']
    return json.dumps(json_obj, ensure_ascii=False)