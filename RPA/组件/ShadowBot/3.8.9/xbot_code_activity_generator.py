from xml.dom.minidom import parse
import xml.etree.ElementTree as ET
import inspect
import sys
import os
import importlib
import argparse

xml_filename = None
node_info = {}
module_names = []

def path_sdk_to_file(name):
    '''
    将sdk的路径转成文件路径
    比如xbot_extensions.sdkcode.modulename.funcname -> xbot_robot.modulename.funcname
    '''
    return '.'.join(['xbot_robot'] + name.split('.')[2:])

def read_xml():
    node_tree = parse(xml_filename)
    root = node_tree.documentElement
    xml_node = root.getElementsByTagName('item')

    for item in xml_node:
        name = item.getAttribute('name')
        #将sdk转成文件相关，并不处理可视化相关: name => xbot-robot.module1.funcname
        name = path_sdk_to_file(name)
        names = name.split('.')
        #可视化流程的文件名均为processxx
        if len(names) == 1 or 'process' not in names[1] :
            #module =>  xbot-robot.module1
            if len(names) <= 2:
                module_names.append(name)
            node_info[name] = ['', '']


def get_info():
    glbs = globals()
    glbs['xbot_robot'] = importlib.import_module('xbot_robot')
    for module in module_names:
        glbs[module] = importlib.import_module(module)

    for key in node_info:
        key_info = eval(key, glbs)
        desc = key_info.__doc__
        node_info[key][0] = '' if desc == None else desc

        try:
            method = inspect.signature(key_info)
            name_array = key.split('.')
            node_info[key][1] = (name_array[-1] + str(method)
                                 ) if len(name_array) > 0 else ''
        except:
            node_info[key][1] = ''


def write_xml():
    doc = ET.parse(xml_filename)
    root = doc.getroot()
    xml_node = root.getchildren()
    loop_xmlnode(xml_node)
    doc.write(xml_filename, encoding='utf-8')


def loop_xmlnode(xml_node):
    for item in xml_node:
        name = item.attrib.get('name')
        if name == None:
            continue
        #将sdk转成文件相关再对比
        name = path_sdk_to_file(name)
        info = node_info.get(name, None)
        if info is None:
            continue
        
        descvalue = info[0]
        item_desc = item.find('item.desc')
        item_desc.text = descvalue

        methodvalue = info[1]
        item_method = item.find('item.method')
        item_method.text = methodvalue

        loop_xmlnode(item.getchildren())

def main():
    parser = argparse.ArgumentParser(allow_abbrev=True)
    parser.add_argument('--file-name', type=str, required=True)
    args, _ = parser.parse_known_args()
    
    global xml_filename
    xml_filename = args.file_name
    read_xml()
    get_info()
    write_xml()

if __name__ == "__main__":
    main()

