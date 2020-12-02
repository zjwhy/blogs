# -*- coding:utf-8 -*-
import inspect
import json
import importlib


def get_method_args(module_name, method_name):
    '''
    动态加载模块 得到方法参数
    :param module_name:  模块名称
    :param method_name:  模块中方法名称
    :return:
    '''
    try:
        module = importlib.import_module(module_name)
        methods = method_name.split(".")
        if (len(methods) == 2):  # 处理对象类
            module = getattr(module, str(methods[0]))
            method_name = methods[1]

        method = getattr(module, method_name) 
        return inspect.signature(method),method.__doc__
    except Exception as es:
        raise es

def fill_params(node,args,doc,module_value,method_value):
    '''
    :param node: 数据节点
    :param args: 参数
    :param doc: doc值
    :param module_value: 模块名称
    :param method_value: 方法
    :return:
    '''

    mode = "static"
    p_args_list = []
    n = 1

    node_items = node["Node"]
    if "Params" not in node_items:
        node["Node"].update({"Params":{}})

    key_list = node["Node"]["Params"].keys()

    for p, pa in args.parameters.items():
        if p == "self":
            mode = 'class'

        if str(p).startswith("*"):
            continue

        ps = str(pa).split('=')
        if len(ps) == 2:

            param = {ps[0]: {}}
            param1 = {}
            if ps[0] in list(node["Node"]["Params"].keys()):
                for key in node["Node"]["Params"][ps[0]].keys():
                    dic = {key:node["Node"]["Params"][ps[0]][key]}
                    dic.update(param1)
                    param1 = dic


            param1.update({"Default": ps[1]} )
            param1.update({"Pos": n})
            param[ps[0]].update(param1)

        else:

            param = {ps[0]: {}}
            param1 = {}
            if ps[0] in list(node["Node"]["Params"].keys()):
                for key in node["Node"]["Params"][ps[0]].keys():
                    dic = {key: node["Node"]["Params"][ps[0]][key]}
                    dic.update(param1)
                    param1 = dic

            param1.update({"Pos": n})
            param[ps[0]].update(param1)

        node["Node"]["Params"].update(param)
        p_args_list.append(p)

        n = n + 1

    node["Node"]['MethodCode']["MethodMode"] = mode
    node["Node"]['MethodCode']["MethodDoc"] = json.dumps(doc, ensure_ascii=False)

    if len(key_list) > 0:
        for index in list(key_list):
            if index not in p_args_list:
                node["Node"]['Params'].pop(index)

    return node

def get_jsondata(file_path):
    '''
    :param file_path: 文件路径
    :return: 获取json格式数据
    '''
    f = None
    try:
        with open(file_path,'r', encoding='utf-8') as f:
            json_data = json.load(f)
    except Exception as e:
        raise
    finally:
        f.close()

    return json_data

def pack_data(data):
    '''
    :param file_path: 文件路径
    :return:
    '''

    #遍历
    for node in data["Nodes"]: 
        module_value = node["Node"]["MethodCode"]["Module"]
        method_value = node["Node"]["MethodCode"]["Method"]

        args,doc = get_method_args(module_value, method_value)

        #组装json格式数据
        fill_params(node,args,doc,module_value,method_value)

    return data

def saveto_newfile(dic_data,file_path):
    '''
    保存新文件
    :param dic_data: 保存数据
    :param file_path:  保存地址
    :return:
    '''
    new_file_path = file_path[:-5] + "build.json"
    f = None

    try:
        with open(new_file_path, 'w') as f:
            json.dump(dic_data, f,indent=4,ensure_ascii=False)  #indent=4 数据保存并格式化
    except Exception as e:
        raise e
    finally:
        f.close()



def do_hand_conf(file_path):

    data = get_jsondata(file_path) 
    
    dic_data = pack_data(data)

    saveto_newfile(dic_data,file_path)















