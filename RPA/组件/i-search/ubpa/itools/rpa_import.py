# -*- coding: utf-8 -*-


import importlib.util 
import os


def import_global_fun(file_path):  
    module_file_path = os.path.abspath(os.path.join(os.path.dirname(file_path), "."))+os.sep+"GlobalFun.py" 
    module_spec = importlib.util.spec_from_file_location(
        "GlobalFun", module_file_path
    )
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)  
    return module

 