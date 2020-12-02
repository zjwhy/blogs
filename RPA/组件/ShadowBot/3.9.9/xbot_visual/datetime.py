import datetime

from ._core import visual_action,parseint_from_args

def get_format(format):
    if format == "YYYY/mm/dd":
        return "%Y/%m/%d"
    elif format == "YYYY年mm月dd日":
        return "%Y年%m月%d日"
    elif format == "HH:MM":
        return "%H:%M"
    elif format == "HH:MM:SS":
        return "%H:%M:%S"
    elif format == "YYYY年mm月dd日 HH:MM":
        return "%Y年%m月%d日 %H:%M"
    elif format == "YYYY年mm月dd日 HH:MM:SS":
        return "%Y年%m月%d日 %H:%M:%S"
    elif format == "YYYY/mm/dd HH:MM":
        return "%Y/%m/%d %H:%M"
    elif format == "YYYY/mm/dd HH:MM:SS":
        return "%Y/%m/%d %H:%M:%S"
    elif format == "YYYY-mm-dd HH:MM:SS":
        return "%Y-%m-%d %H:%M:%S"
    elif format == "YYYY-mm-ddTHH:MM:SS":
        return "%Y-%m-%dT%H:%M:%S"
    else:
        return format

@visual_action
def from_string(**args):
    '''
    功能：字符串转换到日期时间
    '''
    text =  args['text']
    is_custom_format = args['is_custom_format']
    format = get_format(args['format'])

    if is_custom_format:
        return datetime.datetime.strptime(text, format)
    else:
        return datetime.datetime.fromisoformat(text)        

@visual_action
def to_string(**args):
    '''
    功能：日期时间转换到字符串
    '''
    dt = args['datetime']
    format = get_format(args['format'])

    return dt.strftime(format.encode('unicode_escape').decode('utf8')).encode('utf-8').decode('unicode_escape')

@visual_action
def now(**args):
    '''
    功能：获取当前时间
    '''
    return datetime.datetime.now()

@visual_action
def add(**args): 
    '''
    功能：时间相加
    '''
    dt = args['datetime']
    duration = parseint_from_args(args, 'duration')
    unit = args['unit']

    new_dt = datetime.datetime.now()

    if unit == 'second':
        new_dt = dt + datetime.timedelta(seconds=duration)
    elif unit == 'minute':
        new_dt = dt + datetime.timedelta(minutes=duration)
    elif unit == 'hour':
        new_dt = dt + datetime.timedelta(hours=duration)
    elif unit == 'day':
        new_dt = dt + datetime.timedelta(days=duration)
    elif unit == 'month':
        all_month = dt.year * 12 + dt.month + duration
        month = all_month % 12
        year = int(all_month / 12)
        if month == 0:
            year -= 1
            month = 12
        new_dt = datetime.datetime(year, month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)
    elif unit == 'year':
        new_dt = datetime.datetime(dt.year + duration, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)
    else:
        raise ValueError('增量时间单位不正确')

    return new_dt

@visual_action
def difference(**args): 
    '''
    功能：计算时间差差
    '''
    begin_datetime = args['begin_datetime']
    end_datetime = args['end_datetime']
    unit = args['unit']

    seconds = (end_datetime - begin_datetime).total_seconds()
    if unit == 'second':
        return int(seconds)
    elif unit == 'minute':
        return int(seconds / 60)
    elif unit == 'hour':
        return int(seconds / (60 * 60))
    elif unit == 'day':
        return int(seconds / (24 * 60 * 60))
    else:
        raise ValueError('时间差距单位不正确')


class DateTimeParts(object):
    def __init__(self, year, month, day, hour, minute, second):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second


@visual_action
def get_parts(**args):
    '''
    功能：获取年月日时分秒
    '''
    dt = args['datetime']

    if isinstance(dt, (datetime.datetime)):
        pass
    elif isinstance(dt, (str)):
        dt = datetime.datetime.fromisoformat(dt)
    else:
        raise ValueError('输入的数据不是日期时间或者字符串类型')

    return DateTimeParts(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)