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
import sys
import re
import json
from ubpa.ilog import Locallog
import operator
import getopt
Analysislog = Locallog('RPAIanalysis')
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
# {
#     "errcode": 0,
#     "errmsg": "ok",
#     "errors": [{
#         "name": "name-error",
#         "row": 32,
#         "col": 23
#     }, {
#         "name": "attribute-error",
#         "row": 32,
#         "col": 23
#     }],
#     "time": 0.3893891244332844
# }  


def analysis(source=None, path=None, **kwargs):
    data = {"errcode": 0, "errmsg": "ok"}
    data["errors"] = []
    starttime = time.clock() 
    try:
        opts = ''
        if sys.argv.__len__() != 1:  # C++ 通过cmd命令行调用，sys.argv接收命令中包含的参数
            try:
                argv = sys.argv[1:]
                opts, args = getopt.getopt(argv, "hs:p:", ["help", "src=", "path="])
            except getopt.GetoptError:
                print('ianalysis.py -s <src> -p <path>')
            for opt, arg in opts:
                if opt in ('-h', '--help'):
                    print('icomplete.py -s <src> -p <path>')
                    sys.exit()
                elif opt in ("-s", "--src"):
                    source = arg
                elif opt in ("-p", "--path"):
                    path = arg

        message = 'received: ' + '[source=' + str(source) + '],[path=' + str(path) + ']'
        Analysislog.logger.debug(message)
        if source == 'None':
            source = None
        if path == 'None':
            path = None
        script = jedi.Script(source=source, path=path)
        errors = set(repr(e) for e in script._analysis())
        error_name = ''
        row = ''
        col = ''
        temp_list = []
        for error in errors:
            error_pattern = re.compile(r'<Error (.+): .:')
            m = error_pattern.findall(error)
            if len(m) != 0:
                error_name = m[0]

            row_col_pattern = re.compile(r'@(.*),(.*)>')
            m = row_col_pattern.findall(error)
            if len(m) != 0 and len(m[0]) == 2:
                row = int(m[0][0])
                col = int(m[0][1])

            temp_dict = {"name": error_name, "row": row, "col": col,"NodeRow":"","Flow":"","StepNodeTag":"","Note":""}
            with open(file=path,encoding='utf-8') as f:
                fp = f.readlines()
                fp_len = len(fp)
            if row == fp_len:
                list = [row-2, row-3]
            elif (row + 1) == fp_len:
                list = [row-2, row-3, row]
            else:
                list = [row-2, row-3, row, row+1]
            for row in list:
                if 'Flow' in fp[row] and "StepNodeTag" in fp[row] and "Note" in fp[row]:
                    NodeRow_pattern = re.compile('(Flow.*)\'\)')
                    NodeRow = NodeRow_pattern.findall(fp[row])
                    if len(NodeRow) == 1:
                        temp_dict["NodeRow"] = NodeRow[0]

                    Flow_pattern = re.compile('Flow:(.*),StepNodeTag')
                    Flow = Flow_pattern.findall(fp[row])
                    if len(Flow) == 1:
                        temp_dict["Flow"] = Flow[0]

                    StepNodeTag_pattern = re.compile('StepNodeTag:(.*),Note')
                    StepNodeTag = StepNodeTag_pattern.findall(fp[row])
                    if len(StepNodeTag) == 1:
                        temp_dict["StepNodeTag"] = StepNodeTag[0]

                    Note_pattern = re.compile('Note:(.*)\'\)')
                    Note = Note_pattern.findall(fp[row])
                    if len(Note) == 1:
                        temp_dict["Note"] = Note[0]
                    break

            temp_list.append(temp_dict)
        temp_list = sorted(temp_list, key=operator.itemgetter('row'))
        data["errors"] = temp_list
    except Exception as e:
        data['errcode'] = -1
        data['errmsg'] = str(e)
    finally:  
        endtime = time.clock()
        data["time"] = round(endtime - starttime, 2)
        return_data = json.dumps(data)
        print(return_data)
        Analysislog.logger.debug('return :' + return_data)
        return return_data


if __name__ == '__main__':
    analysis()
    #D:\work\data\plugin\Com.Isearch.Func.Python\python.exe D:\work\src\python\src\ubpa\ijedi\ianalysis.py -s None -p D:\work\src\python\src\ubpa\ijedi\ipy.py

# async=1   -->   ExprStmt: 1