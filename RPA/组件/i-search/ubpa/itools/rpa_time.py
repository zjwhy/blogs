# -*- coding: utf-8 -*-
'''
RPA 对时间的处理
'''
import datetime
import time
from ubpa.ilog import ILog
__logger = ILog(__file__)


def get_current_datetime_str(format="%Y-%m-%d"):
    '''
        get_current_datetime_str(format="%Y-%m-%d") -> str
        功能：
            以规定格式返回当前日期
        参数：
            format= "%Y-%m-%d"  输出的格式
        返回:
            规定格式的当前时间
        例子:
             get_current_datetime_str(format= "%Y-%m-%d") -> "2018-05-21"
    '''
    __logger.echo_msg(u"ready to execute[get_current_datetime_str]")
    try:
        today = time.strftime(format, time.localtime())
        return today
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[get_current_datetime_str]")


def get_datetime_to_str(date_time, format="%Y-%m-%d"):
    '''
     get_datetime_to_str(date_time, format= "%Y-%m-%d")-> str
           功能：  将输入的时间 以规定的格式输出
           参数：
                   date_time: 输入的时间
                   format: 要输出的时间格式
           返回：
                   符合规定格式的时间
           例子：
                   get_datetime_to_str("2018-05-21", format= "%Y-%m-%d") -> "2018-05-01"
     '''
    __logger.echo_msg(u"ready to execute[get_datetime_to_str]")
    try:
        str_datetime = datetime.datetime.strftime(date_time, format)
        return str_datetime
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[get_datetime_to_str]")


def dete_dalta_days(dt1, dt2, format1="%Y-%m-%d", format2="%Y-%m-%d"):
    '''
    dete_dalta_days(dt1, dt2, format1="%Y-%m-%d" , format2="%Y-%m-%d") -> int
        功能：输入符合规定模式的2个日期，计算2个日期间隔的日期差
        参数:
              dt1: %y -%m -%d    2018-01-05
              dt2: %y -%m -%d    2018-05-21
        返回：
              2个日期间隔的日期差
        例子：
              dt1:"2018-01-05"      dt2:"2018-11-25"     return : 324
    '''
    __logger.echo_msg(u"ready to execute[dete_dalta_days]")
    try:
        timeArray1 = time.strptime(dt1, format1)
        timeArray2 = time.strptime(dt2, format2)
        d1 = datetime.datetime(timeArray1.tm_year, timeArray1.tm_mon, timeArray1.tm_mday)
        d2 = datetime.datetime(timeArray2.tm_year, timeArray2.tm_mon, timeArray2.tm_mday)
        days = (d2 - d1).days
        return days
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[dete_dalta_days]")


def dete_dalta(days, date=None, format="%Y-%m-%d", return_format="%Y-%m-%d"):
    '''
    dete_dalta(days, date=None, format="%Y-%m-%d", return_format="%Y-%m-%d") -> str
        功能：输入符合规定模式的日期，默认当前日期，计算前n天，后n天的日期
        参数：
            days：相隔的天数
            date：None 默认当前日期
        返回 ：
            wanted_date : 前n天，后n天的日期
        例子：
            dete_dalta(days, date=None, format="%Y-%m-%d", return_format="%Y-%m-%d") -> str
                days=1   date=2018-05-21  return 2018-05-22   后1天
                days=-1  date=2018-05-21  return 2018-05-20   前1天
    '''
    __logger.echo_msg(u"ready to execute[dete_dalta]")
    try:
        if date == None:
            wanted_date = (datetime.datetime.now() + datetime.timedelta(days)).strftime(return_format)
        else:
            date_input = datetime.date.fromtimestamp(time.mktime(time.strptime(date, format)))
            wanted_date = (date_input + datetime.timedelta(days)).strftime(return_format)
        return wanted_date
    except Exception as e:
        raise e
    finally:
        __logger.echo_msg(u"end execute[dete_dalta]")


def get_date_time(format="%Y-%m-%d %H:%M:%S"):
    '''
    get_date_time(format="%Y-%m-%d %H:%M:%S") -> str
        function：Get current system date and time
        return：
              current system date and time
        instance：
            get_date_time("%Y-%m-%d %H:%M:%S")   ->  2019-03-09 13:49:11
    '''
    __logger.debug(u"ready to execute[get_date_time]")
    try:
        result = datetime.datetime.now().strftime(format)
        return result
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[get_date_time]")


def get_current_time(format="%H:%M:%S"):
    '''
        get_current_time(format="%H:%M:%S") -> str
            function：Get current system time
            return：
                  current system time
            instance：
                get_current_time(format="%H:%M:%S")   ->  13:49:11
    '''
    __logger.debug(u"ready to execute[get_current_time]")
    try:
        result = datetime.datetime.now().strftime(format)
        return result
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[get_current_time]")


def datestr_to_datatime(date_str=None, format="%Y-%m-%d %H:%M:%S"):
    '''
    datestr_to_datatime(date_str=None, format="%Y-%m-%d %H:%M:%S") -> <class 'datetime.datetime'>
        function：Convert a time string to a time object
        return：
              <class 'datetime.datetime'>
        instance：
            datestr_to_datatime(date_str = "2016-11-30 13:53:59", format="%Y-%m-%d %H:%M:%S")  ->  2016-11-30 13:53:59
    '''
    result = datetime.datetime.strptime(date_str, format)
    return result


def get_year(datatime_obj=None):
    '''
        get_year(datatime_obj=None) -> str
            function：Get current year
            parameter：
                  datatime_obj : None
                    datatime_obj is a datetime.datetime object, not a string, which can be obtained by datestr_to_datatime()
            return：
                  current year
            instance：
                get_year()  ->  2019
                get_year('2019-04-10 08:10:30') -> 2019

    '''
    __logger.debug(u"ready to execute[get_year]")
    try:
        if datatime_obj == None:
            result = datetime.datetime.now().strftime('%Y')
        else:
            result = datatime_obj.strftime('%Y')
        return result
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[get_year]")


def get_month(datatime_obj=None):
    '''
        get_month(datatime_obj=None) -> str
            function：Get current month
            parameter：
                  datatime_obj : None
                    datatime_obj is a datetime.datetime object, not a string, which can be obtained by datestr_to_datatime()
            return：
                  current month
            instance：
                get_month()  ->  03
                get_month('2019-04-10 08:10:30') -> 4
    '''
    __logger.debug(u"ready to execute[get_month]")
    try:
        if datatime_obj == None:
            result = datetime.datetime.now().strftime('%m')
        else:
            result = datatime_obj.strftime('%m')
        return result
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[get_month]")


def get_day(datatime_obj=None):
    '''
        get_day(datatime_obj=None) -> str
            function：Get current date
             parameter：
                  datatime_obj : None
                    datatime_obj is a datetime.datetime object, not a string, which can be obtained by datestr_to_datatime()
            return：
                  current date
            instance：
                get_day()  ->  09
                get_day('2019-04-10 08:10:30') -> 10
    '''
    __logger.debug(u"ready to execute[get_day]")
    try:
        if datatime_obj == None:
            result = datetime.datetime.now().strftime('%d')
        else:
            result = datatime_obj.strftime('%d')
        return result
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[get_day]")


def get_hour(datatime_obj=None):
    '''
        get_hour(datatime_obj=None) -> str
            function：Get current hour
             parameter：
                  datatime_obj : None
                    datatime_obj is a datetime.datetime object, not a string, which can be obtained by datestr_to_datatime()
            return：
                  current hour
            instance：
                get_hour()  ->  13
                get_hour('2019-04-10 08:10:30') -> 8
    '''

    __logger.debug(u"ready to execute[get_hour]")
    try:
        if datatime_obj == None:
            result = datetime.datetime.now().strftime('%H')
        else:
            result = datatime_obj.strftime('%H')
        return result
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[get_hour]")


def get_minute(datatime_obj=None):
    '''
        get_minute(datatime_obj=None) -> str
            function：Get current minute
            parameter：
                  datatime_obj : None
                    datatime_obj is a datetime.datetime object, not a string, which can be obtained by datestr_to_datatime()
            return：
                  current minute
            instance：
                get_minute()  ->  54
                get_minute('2019-04-10 08:15:30') -> 15
    '''
    __logger.debug(u"ready to execute[get_minute]")
    try:
        if datatime_obj == None:
            result = datetime.datetime.now().strftime('%M')
        else:
            result = datatime_obj.strftime('%M')
        return result
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[get_minute]")


def get_second(datatime_obj = None):
    '''
        get_second(datatime_obj =None) -> str
            function：Get current second
            parameter：
                  datatime_obj : None
                    datatime_obj is a datetime.datetime object, not a string, which can be obtained by datestr_to_datatime()
            return：
                  current second
            instance：
                get_second()  ->  54
                get_second('2019-04-10 08:15:30') -> 30
    '''
    __logger.debug(u"ready to execute[get_second]")
    try:
        if datatime_obj == None:
            result = datetime.datetime.now().strftime('%S')
        else:
            result = datatime_obj.strftime('%S')
        return result
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[get_second]")


def get_weekday():
    '''
        get_weekday() -> str
            function：Get today is the day of the week
            return：
                  the day of the week
            instance：
                1  : Monday
                2  : Tuesday
                3  : Wednesday
                4  : Thursday
                5  : Friday
                6  : Saturday
                7  : Sunday
    '''
    __logger.debug(u"ready to execute[get_weekday]")
    try:
        d = datetime.datetime.now()
        result = d.weekday()
        return str(result + 1)
    except Exception as e:
        raise e
    finally:
        __logger.debug(u"end execute[get_weekday]")

