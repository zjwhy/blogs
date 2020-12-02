# -*- coding:utf-8 -*-
'''
Created on 2019,1

@author: Wu.Xin
'''
# source=None, line=None, column=None, path=None,
#                  encoding='utf-8', sys_path=None, environment=None
#
import time
import jedi
import os, logging
import json
import sys
import operator
import getopt
# :param source: The source code of the current file, separated by newlines.
#     :type source: str
#     :param line: The line to perform actions on (starting with 1).
#     :type line: int
#     :param column: The column of the cursor (starting with 0).
#     :type column: int
#     :param path: The path of the file in the file system, or ``''`` if
#         it hasn't been saved yet.
#     :type path: str or None
#     :param encoding: The encoding of ``source``, if it is not a
#         ``unicode`` object (default ``'utf-8'``).
#     :type encoding: str
#     :param sys_path: ``sys.path`` to use during analysis of the script
#     :type sys_path: list
#     :param environment: TODO
#     :type sys_path: Environment
#    {
#     "errcode": 0,
#     "errmsg": "ok",
#       "time": 23,
#     "completions": [{
#         "type": "function",
#         "name": "tclass",
#         "params": "abc='123',abc='123'"
#     }, {
#         "type": "statement",
#         "name": "p1"
#     }, {
#         "type": "module",
#         "name": "p1"
#     }]
# }
from ubpa.ilog import Locallog
Completelog = Locallog('RPAIcomplete')


def complete(source=None, path=None, line=None, column=None, **kwargs):
    opts = ''
    if sys.argv.__len__() != 1:    #  C++ 通过cmd命令行调用，sys.argv接收命令中包含的参数
        try:
            argv = sys.argv[1:]
            opts, args = getopt.getopt(argv, "hs:p:l:c:", ["help", "src=", "path=", "line=", "column="])
        except getopt.GetoptError:
                print('icomplete.py -s <src> -p <path> -l <line> -c <column>')
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print('icomplete.py -s <src> -p <path> -l <line> -c <column>')
                sys.exit()
            elif opt in ("-s", "--src"):
                source = arg
            elif opt in ("-p", "--path"):
                path = arg
            elif opt in ("-l", "--line"):
                line = arg
            elif opt in ("-c", "--column"):
                column = arg
    message = 'received: '+ '[source=' + str(source) + '],[path=' + str(path) + '],[line=' + str(line) + '],[column='+ str(column) + ']'
    Completelog.logger.debug(message)
    data = {"errcode": 0, "errmsg": "ok"}
    data["completions"] = []
    starttime = time.clock()
    try:
        if source == 'None':
            source = None
        if path == 'None':
            path = None
        script = jedi.Script(source=source, path=path, line=int(line), column=int(column))
        completions = script.completions()
        temp_list = []
        for c in completions:
            if not c.name.startswith('__'):
                temp = {"type": c.type, "name": c.name}
                if hasattr(c, 'params'):
                    final_param = ''
                    for param in c.params:
                        if '=' in param.description:  # " abc='123', def='456' "
                            param_value = param.description.split('=')[1]
                            single_param_value = str(param.name) + '=' + param_value
                        else:                         # "abc, def='123'"
                            single_param_value = str(param.name)
                        if single_param_value != "" or None:
                            final_param = final_param + ',' + single_param_value
                    final_param = final_param[1:]
                    temp.update({"params": '(' + final_param + ')'})
                temp_list.append(temp)

        temp_list = sorted(temp_list, key=operator.itemgetter('name'))
        data["completions"] = temp_list

    except Exception as e:
        data['errcode'] = -1
        data['errmsg'] = str(e)
    finally:
        endtime = time.clock()
        data["time"] = round(endtime-starttime, 2)
        return_data = json.dumps(data)
        print(return_data)
        Completelog.logger.debug('return: ' + return_data)
        return return_data


if __name__ == '__main__':
    complete()

    # D:\work\data\plugin\Com.Isearch.Func.Python\python.exe D:\work\src\python\src\ubpa\ijedi\icomplete.py -s None -p C:\Users\DELL\Desktop\my.py -l 22 -c 13
    # D:\work\data\plugin\Com.Isearch.Func.Python\python.exe D:\work\src\python\src\ubpa\ijedi\icomplete.py -s None --path C:\Users\DELL\Desktop\my.py -l 22 -c 13
    # D:\work\data\plugin\Com.Isearch.Func.Python\python.exe D:\work\src\python\src\ubpa\ijedi\icomplete.py -s None --path=C:\Users\DELL\Desktop\my.py -l 22 -c 13
