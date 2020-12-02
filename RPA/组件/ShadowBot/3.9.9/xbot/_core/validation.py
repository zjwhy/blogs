from enum import Enum, unique


@unique
class ValidPattern(Enum):
    NotNone = 0
    NotEmpty = 1
    Type = 2
    Min = 3
    Max = 4
    Range = 5
    NotEmptyArray = 6


def valid_multi(name, value, patterns):
    for pattern in patterns:
        valid(name, value, pattern)


def valid(name, value, pattern):
    if isinstance(pattern, tuple):
        pname, pargs = pattern
    else:
        pname, pargs = pattern, None
    if pname == ValidPattern.NotNone:
        if value is None:
            raise ValueError(f'{name}参数不能为None')
    elif pname == ValidPattern.NotEmpty:
        if value is None or value == '':
            raise ValueError(f'{name}参数不能为空')
    elif pname == ValidPattern.Type:
        if not isinstance(value, pargs):
            raise ValueError(f'{name}参数类型错误')
    elif pname == ValidPattern.Min:
        if not isinstance(value, (int, float)):
            raise ValueError(f'{name}参数必须为数字类型')
        if value < pargs:
            raise ValueError(f'{name}参数必须大于{pargs}')
    elif pname == ValidPattern.Max:
        if not isinstance(value, (int, float)):
            raise ValueError(f'{name}参数必须为数字类型')
        if value > pargs:
            raise ValueError(f'{name}参数必须小于{pargs}')
    elif pname == ValidPattern.Range:
        if not isinstance(value, (int, float)):
            raise ValueError(f'{name}参数必须为数字类型')
        if not (value >= pargs[0] and value <= pargs[1]):
            raise ValueError(f'{name}参数必须在{pargs[0]}和{pargs[1]}之间')
    elif pname == ValidPattern.NotEmptyArray:
        if value is None or value == []:
            raise ValueError(f'{name}参数不能为空')
    else:
        pass
