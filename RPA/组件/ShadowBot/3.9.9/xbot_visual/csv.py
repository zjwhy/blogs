from ._core import visual_action, parseint_from_args
import csv, os

@visual_action
def read(**args):
    csv_path = args['csv_path']
    encoding = args['encoding']
    first_row_is_header = args['first_row_is_header']

    if not os.path.exists(csv_path):
        raise ValueError(f'文件 {csv_path} 不存在！')

    values = []
    first_row = True
    with open(csv_path, 'r', encoding=encoding) as f:
        reader = csv.reader(f)
        for row in reader:
            if first_row and first_row_is_header:
                first_row = False
            else:
                values.append(row)

    return values


@visual_action
def write(**args):
    csv_path = args['csv_path']
    encoding = args['encoding']
    write_way = args['write_way']
    values = args['values']

    if not isinstance(values, (list)):
        raise ValueError('待写入的数据不是列表！')
    
    all_elem_is_list = True
    for elem in values:
        if not isinstance(elem, (list)):
            all_elem_is_list = False
            break
    if not all_elem_is_list:
        values = [values]

    mode = ''
    if write_way == 'append':
        mode = 'a'
    elif write_way == 'overwrite':
        mode = 'w'

    with open(csv_path, mode, encoding=encoding, newline='') as f:
        writer = csv.writer(f)
        writer.writerows(values)