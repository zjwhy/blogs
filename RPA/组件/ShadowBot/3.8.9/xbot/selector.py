'''
元素选择器模块
'''
from ._core import try_get_sdmodule

import re
import os
import inspect
import numbers

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

_NS_X = "{rpa://selector/core}"
_NS_REGEX = "{rpa://selector/operator/regex}"
_NS_WILDCARD = "{rpa://selector/operator/wildcard}"
global_variable_pattern = re.compile(r"^\s*{{([a-zA-Z_\u4e00-\u9eff][a-zA-Z0-9_\u4e00-\u9eff]*)}}\s*$")



def _get_selector_by_name(selector_name):
    sdmodule = try_get_sdmodule()
    selector_func = sdmodule['selector']
    if selector_func is None:
        return None
    else:
        return selector_func(selector_name)


def _get_image_selector_by_name(image_selector_name):
    sdmodule = try_get_sdmodule()
    selector_func = sdmodule['image_selector']
    if selector_func is None:
        return None
    else:
        return selector_func(image_selector_name)


def _replace_ascii_control_code(filepath):
    """替换ASCII control characters"""
    pattern = r"&#(\d+|x\w{2});"  # &#x1E;          &#030;
    repl_pattern = "%_%\\1%_%"  # %_%x1E%_%       %_%030%_%
    with open(filepath, 'r', encoding='utf8') as xmlfile:
        content = xmlfile.read()
    result = re.sub(pattern, repl_pattern, content, 0, re.MULTILINE)
    return result


def _restore_ascii_control_code(value):
    """将格式化后的控制符转换为实际的字符"""

    def repl_pattern(match):
        value = match.group(1)  # x1E、030
        if value[0] == 'x':
            return chr(int(value[1:], 16))
        else:
            return chr(int(value))

    pattern = r"%_%([^%]+)%_%"  # %_%x1E%_%       %_%030%_%
    result = re.sub(pattern, repl_pattern, value, 0, re.MULTILINE)
    return result

def _replace_global_variable(value):
    """
    替换全局变量，类似 {{value}
    """
    def _repl_pattern(matcher):
        sdmodule = try_get_sdmodule()
        variable_dict = sdmodule['variables']
        variable_value = variable_dict[matcher.group(1)]
        if isinstance(variable_value, str) or (isinstance(variable_value, numbers.Number) and not isinstance(variable_value, bool)):
            return str(variable_value)
        elif variable_value is None:
            return ""
        else:
            raise ValueError('元素中的全局变量只能是字符串或数字类')

    matchers = global_variable_pattern.findall(value)
    if matchers:
        value = global_variable_pattern.sub(_repl_pattern, value)
    return value
 
class Selector():
    def __init__(self, value):
        self.value = value


class TableSelector():
    def __init__(self, value):
        self.value = value


# selectors.xml读取逻辑:
# 1. 读取文件，并替换所有ASCII控制符，防止 &#x1E; 这样的字符导致xml加载失败，统一格式化成 %_%x1E%_%   ==>   _replace_ascii_control_code
# 2. 查找元素，在返回Selector前，把Selector属性值替换成原生的ASCII字符   ==>   _restore_ascii_control_code
# 场景：https://subway.simba.taobao.com/indexnew.jsp 中的用户名控件
class SelectorStore():

    def __init__(self, app_folder):
        filepath = os.path.join(app_folder, 'selectors.xml')
        xml_str = _replace_ascii_control_code(filepath)
        self._tree = et.fromstring(xml_str)

    def __call__(self, name):
        selector_ele = self._tree.find(
            f'selector[@name="{name}"]')
        if selector_ele is None:
            return None
        selector = selector_ele.attrib.copy()
        if selector['type'] == 'table':  # table selector
            for child_ele in selector_ele:  # <base> or <columns>
                if child_ele.tag == 'base':
                    selector['base'] = []
                    for node_ele in child_ele:  # <base>/<web>
                        selector_node = self._resolve_selector_node_from_xml(
                            node_ele)
                        selector['base'].append(selector_node)
                elif child_ele.tag == 'columns':
                    selector['columns'] = []
                    for column_ele in child_ele:  # <columns>/<column>
                        selector_column = column_ele.attrib.copy()
                        selector_column['path'] = []
                        for node_ele in column_ele:  # <columns>/<column>/<web>
                            selector_node = self._resolve_selector_node_from_xml(
                                node_ele)
                            selector_column['path'].append(selector_node)
                        selector['columns'].append(selector_column)
                else:
                    pass
            return TableSelector(selector)
        else:  # simple selector
            selector['path'] = []
            for node_ele in selector_ele:
                selector_node = self._resolve_selector_node_from_xml(node_ele)
                selector['path'].append(selector_node)
            return Selector(selector)

    def _resolve_selector_node_from_xml(self, xml_node):
        selector_node = {
            'name': xml_node.attrib[f'{_NS_X}name'],
            'type': xml_node.tag,
            'attributes': []
        }
        for attr_name, attr_value in xml_node.attrib.items():
            ns, attr_name = re.match(r"^({[^}]+})?(.*)$", attr_name).groups()
            if ns is None:
                attr_operator = 'Equal'
            elif ns == _NS_REGEX:
                attr_operator = 'Regex'
            elif ns == _NS_WILDCARD:
                attr_operator = 'WildCard'
            else:
                # 可能是"x:"，应该在上层处理，这里忽略
                continue
            attr_value = _restore_ascii_control_code(attr_value)
            #替换变量
            attr_value = _replace_global_variable(attr_value)
            selector_node['attributes'].append({
                'name': attr_name,
                'value': attr_value,
                'required': True,
                'operator': attr_operator
            })
        return selector_node


class ImageSelectorStore():

    def __init__(self, app_folder):
        filepath = os.path.join(app_folder, 'images.xml')
        self._tree = et.ElementTree(file=filepath)
        self.app_folder = app_folder

    def __call__(self, name):
        image_ele = self._tree.find(
            f'imageelement[@name="{name}"]')
        if image_ele is None:
            return None
        image = image_ele.attrib.copy()
        image['filepath'] = os.path.join(
            self.app_folder, image['filepath'])    # 相对路径 -> 绝对路径
        return ImageSelector(image)


class ImageSelector():
    def __init__(self, value):
        self.value = value
