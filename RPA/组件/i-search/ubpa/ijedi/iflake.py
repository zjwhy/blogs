# -*- coding:utf-8 -*-

import sys
import getopt
import time
from pyflakes import api
import json
import re

# param: need a path to analysis the error or warning in file
# return: {
#     "errcode":0,
#     "errmsg":"ok",
#     "errors":[
#         {
#             "name":"unexpected EOF while parsing",
#             "row":181,
#             "col":15,
#             "node_row":null,
#             "level": Warn  /  Error,
#             "flow":null,
#             "step_node_tag":null,
#             "note":null
#         }
#     ],
#     "time":0
# }


from ubpa.ilog import Locallog

Flakelog = Locallog('RPAIflake')


def ianalysises(path=None):
    data = {"errcode": 0, "errmsg": "ok", "errors": []}
    path_list = []

    if sys.argv.__len__() != 1:
        try:

            argv = sys.argv[1:]
            opts, args = getopt.getopt(argv, "hp:", ["help", "path="])
        except getopt.GetoptError:
                print('error: iflake.py -p <path>')

        for opt, arg in opts:

            if opt in ('-h', '--help'):
                sys.exit()
            elif opt in ("-p", "--path"):
                path = arg

        Flakelog.logger.debug('received: ' + '[path=' + str(path) + ']')
    try:
        starttime = time.clock()

        path_list.append(path)
        wrongs = api.main(prog='pyflakes', args=path_list)
        if 1 == wrongs["key1"]:
            # filename = wrongs["filename"]
            msg = wrongs["msg"]
            lineno = wrongs["lineno"]
            offset = wrongs["offset"]
            # text = wrongs["text"]

            fp, fp_len = file_read(path)
            NodeRow, Flow, StepNodeTag, Note = row_ana(fp, fp_len, lineno)

            error_dic = {
                        "name": msg,
                        "row": lineno,
                        "col": offset,
                        "node_row": NodeRow,
                        "level": "Error",
                        "flow": Flow,
                        "step_node_tag": StepNodeTag,
                        "note": Note
                    }

            data["errors"].append(error_dic)

        if 0 == wrongs["key1"]:

            fp, fp_len = file_read(path)
            for wrong in wrongs["message"]:

                # if "is assigned to but never used" in str(wrong):
                #     continue
                # if "imported but unused" in str(wrong):
                #     continue
                # if "unable to detect undefined names" in str(wrong):
                #     continue
                # if "may be undefined, or defined from star imports" in str(wrong):
                #     continue
                # if "redefinition of unused" in str(wrong):
                #     continue
                level = level_grading(str(wrong))
                col = wrong.col  #lie
                lineno = wrong.lineno   #hang
                detail_wrong = str(wrong).replace(wrong.filename+":"+str(lineno)+":", "")
                NodeRow, Flow, StepNodeTag, Note = row_ana(fp, fp_len, lineno)

                error_dic = {
                            "name": detail_wrong,
                            "row": lineno,
                            "col": col,
                            "node_row": NodeRow,
                            "level": level,
                            "flow": Flow,
                            "step_node_tag": StepNodeTag,
                            "note": Note
                        }

                data["errors"].append(error_dic)
    except Exception as e:
        data['errcode'] = -1
        data['errmsg'] = str(e)
    finally:
        endtime = time.clock()
        data["time"] = round(endtime - starttime, 2)
        print(json.dumps(data))
        Flakelog.logger.debug('return: ' + json.dumps(data))
        return json.dumps(data)

def file_read(path):
    try:
        with open(file=path, encoding='utf-8') as f:
            fp = f.readlines()
            fp_len = len(fp)

        return fp, fp_len
    except Exception as e:
        raise e


def row_ana(fp, fp_len, row):

    NodeRow = None
    Flow = None
    StepNodeTag = None
    Note = None
    try:
        if row == fp_len:
            list = [row - 2, row - 3]
        elif (row + 1) == fp_len:
            list = [row - 2, row - 3, row]
        else:
            list = [row - 2, row - 3, row, row + 1]
        for row in list:
            if row >=0 :
                if "self.__logger.debug('Flow:" in fp[row]:
                    NodeRow_pattern = re.compile('(Flow.*)\'\)')
                    NodeRow = NodeRow_pattern.findall(fp[row])
                    if len(NodeRow) == 1:
                        NodeRow = NodeRow[0]

                    Flow_pattern = re.compile('Flow:(.*),StepNodeTag')
                    Flow = Flow_pattern.findall(fp[row])
                    if len(Flow) == 1:
                        Flow = Flow[0]

                    StepNodeTag_pattern = re.compile('StepNodeTag:(.*),Note')
                    StepNodeTag = StepNodeTag_pattern.findall(fp[row])
                    if len(StepNodeTag) == 1:
                        StepNodeTag = StepNodeTag[0]

                    Note_pattern = re.compile('Note:(.*)\'\)')
                    Note = Note_pattern.findall(fp[row])
                    if len(Note) == 1:
                        Note = Note[0]
                    break

        return NodeRow, Flow, StepNodeTag, Note
    except Exception as e:
        raise e


def level_grading(wrong):
    if "imported but unused" in str(wrong):
        return "Warn"
    elif "unable to detect undefined names" in str(wrong):
        return "Warn"
    elif "redefinition of unused" in str(wrong):
        return "Warn"
    else:
        return "Error"

if __name__ == '__main__':
#     path = r"C:\Users\DELL\Desktop\jdei_analysis_testcode\Main_ytt.py"
     ianalysises()
#     print(cc)
