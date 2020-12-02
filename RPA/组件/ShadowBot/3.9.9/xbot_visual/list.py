from ._core import visual_action, parseint_from_args
import random
from xbot._core.validation import valid, valid_multi, ValidPattern

# 创建 
@visual_action
def create():
    return []

# 删除
@visual_action
def clear(**args):
    """
        'lst':[]
    """
    lst = args['lst']
    valid_multi('列表', lst, (ValidPattern.NotNone, (ValidPattern.Type, list)))
    lst.clear()


# 增
@visual_action
def append(**args):
    """
        'lst':[]
        'elem':0
    """
    lst = args['lst']
    elem = args['elem']
    lst.append(elem)


@visual_action
def extend(**args):
    """
        'lst1':[]
        'lst2':[]
    """
    lst1 = args['lst1']
    lst2 = args['lst2']
    valid_multi('列表1', lst1, (ValidPattern.NotNone, (ValidPattern.Type, list)))
    valid_multi('列表2', lst2, (ValidPattern.NotNone, (ValidPattern.Type, list)))
    return lst1 + lst2


@visual_action
def insert(**args):
    """
        'lst':[]
        'index':0
        'elem':0
    """
    lst = args['lst']
    index = parseint_from_args(args, 'index')
    elem = args['elem']
    lst.insert(index, elem)


@visual_action
def append_or_insert(**args):
    """
        'lst':[]
        'insert_way': 'append' or 'insert'
        'index':*
        'elem':*
    """
    lst = args['lst']
    insert_way = args['insert_way']
    elem = args['elem']

    valid_multi('列表', lst, (ValidPattern.NotNone, (ValidPattern.Type, list)))

    if insert_way == 'append':
        lst.append(elem)
    elif insert_way == 'insert':
        index = parseint_from_args(args, 'index')
        lst.insert(index, elem)
    else:
        raise ValueError('插入方式不合法')


# 删
@visual_action
def remove(**args):
    """
        'lst':[]
        'elem':0
    """
    remove_way = args['remove_way']
    lst = args['lst']
    elem = args['elem']

    valid_multi('列表', lst, (ValidPattern.NotNone, (ValidPattern.Type, list)))

    if remove_way == 'index':
        index = parseint_from_args(args, 'index') 
        try:
            del lst[index]
        except IndexError:
            raise ValueError('下标值超过最大下标')
    elif remove_way == 'elem':
        while elem in lst:
            lst.remove(elem)

    
@visual_action
def remove_duplicate(**args):
    """
        'lst':[]
    """
    lst = args['lst']

    valid_multi('列表', lst, (ValidPattern.NotNone, (ValidPattern.Type, list)))

    lst1 = []
    lst1.extend(lst)

    lst.clear()
    for e in lst1:
        if e not in lst:
            lst.append(e)

    
@visual_action
def remove_list(**args):
    """
        'lst1':[]
        'lst2':[]
    """
    lst1 = args['lst1']
    lst2 = args['lst2']

    valid_multi('列表1', lst1, (ValidPattern.NotNone, (ValidPattern.Type, list)))
    valid_multi('列表2', lst2, (ValidPattern.NotNone, (ValidPattern.Type, list)))

    lst3 = lst1
    for elem in lst2:
        while elem in lst3:
            lst3.remove(elem)

    return lst3


@visual_action
def pop(**args):
    """
        'lst':[]
    """
    lst = args['lst']
    return lst.pop()


@visual_action
def shrink(**args):
    """
        'lst':[]
        'lst1':[]
    """
    lst = args['lst']
    lst1 = args['lst1']
    for elem in lst1:
        if elem in lst:
            lst.remove(elem)


# 改
@visual_action
def set_elem(**args):
    """
        'lst':[]
        'index':0
        'elem':0
    """
    lst = args['lst']
    index = parseint_from_args(args, 'index')
    elem = args['elem']

    lst[index] = elem


# 查
@visual_action
def length(**args):
    """
        'lst':[]
    """
    lst = args['lst']

    return len(lst)


@visual_action
def get_elem(**args):
    """
        'lst':[]
        'index':0
    """
    lst = args['lst']
    index = parseint_from_args(args, 'index')

    valid_multi('列表', lst, (ValidPattern.NotNone, (ValidPattern.Type, list)))

    elem = None
    try:
        elem =lst[index]
    except IndexError:
        raise ValueError('下标值超过最大下标')
    return elem


@visual_action
def get_duplicate(**args):
    """
        'lst1':[]
        'lst2':[]
    """
    lst1 = args['lst1']
    lst2 = args['lst2']

    valid_multi('列表1', lst1, (ValidPattern.NotNone, (ValidPattern.Type, list)))
    valid_multi('列表2', lst2, (ValidPattern.NotNone, (ValidPattern.Type, list)))

    lst3 = []
    for elem in lst1:
        if elem in lst2 and elem not in lst3:
            lst3.append(elem)

    return lst3


@visual_action
def get_index(**args):
    """
        'lst':[]
        'elem':0
    """
    lst = args['lst']
    elem = args['elem']

    valid_multi('列表', lst, (ValidPattern.NotNone, (ValidPattern.Type, list)))

    return lst.index(elem)


# 排序
@visual_action
def sort(**args):
    """
        'lst':[]        
        'sort_way':'descend' or 'ascend'
    """
    lst = args['lst']
    sort_way = args['sort_way']

    valid_multi('列表', lst, (ValidPattern.NotNone, (ValidPattern.Type, list)))

    lst.sort(reverse = True if sort_way == 'descend' else False)

    
@visual_action
def shuffle(**args):
    """
        'lst':[]
    """
    lst = args['lst']

    valid_multi('列表', lst, (ValidPattern.NotNone, (ValidPattern.Type, list)))

    random.shuffle(lst)


# 反转
@visual_action
def reverse(**args):
    """
        'lst':[]
    """
    lst = args['lst']

    valid_multi('列表', lst, (ValidPattern.NotNone, (ValidPattern.Type, list)))

    lst = lst.reverse()


# 列表长度
@visual_action
def get_len(**args):
    """
        'lst':[]
    """
    lst = args['lst']

    valid_multi('列表', lst, (ValidPattern.NotNone, (ValidPattern.Type, list)))

    return len(lst)