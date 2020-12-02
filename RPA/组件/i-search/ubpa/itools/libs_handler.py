# -*- coding:utf-8 -*-
import ast
import json
import os
import sys

def show_info(functionNode,result_dic1):
    func_dic = {}
    args_list = []
    func_args_list = functionNode.args.args
    func_args_list.reverse()
    f_default_list = functionNode.args.defaults
    f_default_list.reverse()

    for j in range(len(func_args_list)):
        if "self" != func_args_list[j].arg:
            args_dic = {}
            param_value = "qazwsxedc"
            param_args = func_args_list[j].arg

            if len(f_default_list) > 0:
                if j < len(f_default_list):
                    param_val = f_default_list[j]
                    if hasattr(param_val,"n"):
                        param_value = param_val.n
                    if hasattr(param_val,"value"):
                        param_value = param_val.value
                    if hasattr(param_val,"s"):
                        param_value = param_val.s
                    if hasattr(param_val,"keys") and hasattr(param_val,"values"):#flow(self,aa={"sa":12,"er":"re"})
                        param_value = {}
                        keys_list = param_val.keys
                        values_list = param_val.values
                        for j in range(len(keys_list)):
                            if hasattr(keys_list[j],"n"):
                                _key = keys_list[j].n
                            if hasattr(keys_list[j],"value"):
                                _key = keys_list[j].value
                            if hasattr(keys_list[j],"s"):
                                _key = keys_list[j].s
                            if hasattr(values_list[j],"n"):
                                _values = values_list[j].n
                            if hasattr(values_list[j],"value"):
                                _values = values_list[j].value
                            if hasattr(values_list[j],"s"):
                                _values = values_list[j].s
                            param_value[_key] = _values
                    if hasattr(param_val,"elts"):  #flow(self,bb=[1,2,"abcd",True]):
                        elts_list = param_val.elts
                        param_value = []
                        for elt in elts_list:
                            if hasattr(elt, "n"):
                                elt_val = elt.n
                            if hasattr(elt, "value"):
                                elt_val = elt.value
                            if hasattr(elt, "s"):
                                elt_val = elt.s
                            param_value.append(elt_val)

            if param_args != "":
                args_dic["Name"] = param_args
            if param_value != "qazwsxedc" and param_value != None:
                if isinstance(param_value, str):
                    args_dic["Value"] = "'"+param_value+"'"
                else:
                    args_dic["Value"] = str(param_value)
            args_list.append(args_dic)
        else:
            if "__init__" == functionNode.name:
                func_body = functionNode.body
                for k in func_body:
                    class_var_dic = {}
                    if "targets" in k._fields:
                        if hasattr(k,"targets"):
                            k_tar = k.targets
                            if len(k_tar) > 0:
                                if hasattr(k_tar[0],"attr"):
                                    class_var_dic["Name"] = k_tar[0].attr
                                    result_dic1["Vars"].append(class_var_dic)

    func_dic["Name"] = functionNode.name
    func_dic["Desc"] = ""
    args_list.reverse()
    func_dic["Params"] = args_list

    result_dic_func = result_dic1["Funs"]
    result_dic_func.append(func_dic)

    return result_dic1


def get_compliments(filename):
    list1 = []
    result_dic1 = {"Info": {"ID": "", "Name": "", "Import": "", "PinYin": "", "Ico": "", "Desc": "", "Pos": 1}, "Funs": [], "Vars": []}
    result_dic2 = {"Info": {"ID": "", "Name": "", "Import": "", "PinYin": "", "Ico": "", "Desc": "", "Pos": 1}, "Funs": [], "Vars": []}

    with open(filename, encoding='utf-8') as file:
        try:
            f = file.read()
            node = ast.parse(f)
        except:
            return []

    all_clas = [n for n in node.body if isinstance(n, ast.ClassDef)]  #类及类中的方法

    project_name = get_projet_name(filename)

    for clas in all_clas:

        result_dic1["Info"]["ID"] = clas.name
        result_dic1["Info"]["Name"] = clas.name
        result_dic1["Info"]["Desc"] = clas.name
        result_dic1["Info"]["Import"] = "from ubpalib." + project_name + ".codes.Main import " + clas.name
        result_dic1["Info"]["PinYin"] = "ubpalib." + project_name + ".codes.Main import " + clas.name
        methods = [j for j in clas.body if isinstance(j, ast.FunctionDef)]
        for method in methods:
            result_dic1 = show_info(method, result_dic1)

        list1.append(result_dic1)
        result_dic1 = result_dic2

    return list1

def get_folder_list(filename):
    file_list = []
    n = 0

    try:

        for root, dirs, files in os.walk(filename):
            n = n + 1
            if n >= 2:
                break
            for dir in dirs:
                dir_path = root + os.sep + dir + os.sep + "codes" + os.sep + "Main.py"
                file_list.append(dir_path)

            # for file_name in files:
            #
            #     full_file_addr = root + os.sep + file_name
            #     exclude_str = os.sep + "codes" + os.sep
            #     if exclude_str in full_file_addr:
            #         file_name = full_file_addr[-7:]
            #         if "Main.py" == file_name:
            #             file_list.append(full_file_addr)
        return file_list
    except Exception as e:
        raise (e)

def get_projet_name(file_name):
    try:
        new_name = os.path.abspath(os.path.join(str(file_name), "../../.."))
        if "/" in file_name and "\\" in new_name:
            new_name = new_name.replace("\\", "/")
        elif "\\" in file_name and "/" in new_name:
            new_name = new_name.replace("/", "\\")
        n_name = str(file_name).replace(new_name, '')[1:]
        new_name_list = n_name.split(os.sep)

        return new_name_list[0]
    except Exception as e:
        raise (e)

def get_file_dic(filename,json_addr):
    list2 = []
    try:
        file_list = get_folder_list(filename)
        for filename in file_list:
            try:
                list1 = get_compliments(filename)
                # robot_dic = {"Robot": list1}
                # list2.append(robot_dic)
                list2 = list2 + list1
            except Exception as e:
                pass
       # str_json = str({"Robots": list2})
        str_json = json.dumps({"Robots": list2}, ensure_ascii=False)
        print(str_json)
        with open(json_addr, 'w', encoding='utf-8') as f:
            f.write(str_json)
        print("qazwsxedc")
        return str_json
    except Exception as e:
        raise (e)



if __name__ == '__main__':

    # filename = r'D:\robotTool2\studio-v6\project'
    # filename = r'D:\robotTool2\plugin\Com.Isearch.Func.Python\Lib\ubpalib'
    # json_addr = r'C:\Users\tanbinbin\Desktop\aa.json'
    filename = sys.argv[1]
    json_addr = sys.argv[2]
    aa = get_file_dic(filename, json_addr)
