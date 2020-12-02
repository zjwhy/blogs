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
import json
import sys
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
#     "time": 23,
#     "defs": [{
#         "type": "function",
#         "module_name":"modulename"
#         "module_path":"d:\abc\aaa.py"
#         "name": "do_click",
#         "line": 89
#     }]
# }
from ubpa.ilog import Locallog

Gotolog = Locallog('RPAIgoto')


def goto():
    opts = ""
    data = {"errcode": 0, "errmsg": "ok", "time": None, "defs": []}

    if sys.argv.__len__() != 1:
        try:

            argv = sys.argv[1:]
            opts, args = getopt.getopt(argv, "hs:p:l:c:", ["help", "src=", "path=", "line=", "column="])
        except getopt.GetoptError:

                print('error: igoto.py -s <src> -p <path> -l <line> -c <column>')
        for opt, arg in opts:

            if opt in ('-h', '--help'):
                print('igoto.py -s <src> -p <path> -l <line> -c <column>')
                sys.exit()
            elif opt in ("-s", "--src"):
                source = arg
            elif opt in ("-p", "--path"):
                path = arg
            elif opt in ("-l", "--line"):
                line = arg
            elif opt in ("-c", "--column"):
                column = arg

        Gotolog.logger.debug('received: ' + '[source=' + str(source) + '],[path=' + str(path) + '],[line=' + str(line) + '],[column='+ str(column) + ']')
        starttime = time.clock()
        try:

            if source == 'None':
                source = None
            if path == 'None':
                path = None

            script = jedi.Script(source=source, path=path, line=int(line), column=int(column))
            assignments = script.goto_assignments(follow_imports=True)

            for assignment in assignments:

                ass_type = assignment.type
                ass_module_name = assignment.module_name
                ass_module_path = assignment.module_path
                ass_name = assignment.name
                ass_line = assignment.line
                ass_dic = {
                            "type": ass_type,
                            "module_name": ass_module_name,
                            "module_path": ass_module_path,
                            "name": ass_name,
                            "line": ass_line
                        }

                data["defs"].append(ass_dic)
        except Exception as e:
            data['errcode'] = -1
            data['errmsg'] = str(e)
        finally:
            endtime = time.clock()
            data["time"] = round(endtime-starttime, 2)
            print(json.dumps(data))
            Gotolog.logger.debug('return: ' + json.dumps(data))
            return json.dumps(data)


if __name__ == '__main__':

    goto()
