# -*- coding:utf-8 -*-
import json

def org_param(param,text,getVal):

    dic = {}
    paramJason = json.loads(param)
    dic[text] = getVal
    paramJason["input"] = dic
    return json.dumps(paramJason,ensure_ascii=False)


 