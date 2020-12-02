'''
数据库自动化模块, 可实现数据库的连接/断开、SQL语句的执行
'''

import win32com.client
import typing

class Database(object):
    '''
    数据库自动化模块, 可实现数据库的连接/断开、SQL语句的执行
    '''

    def open(self, conn_str) -> typing.NoReturn:
        '''
        打开连接数据库
        * @param conn_str, 数据库连接字符串, 如: Provider=MSDASQL.1;Persist Security Info=False;Data Source=数据库连接名
        '''

        self.conn = win32com.client.Dispatch(r"ADODB.connection")
        self.conn.Open(conn_str)

    def exec(self, sql, timeout_seconds=20) -> typing.List[typing.List[str]]:
        '''
        执行SQL语句
        * @param sql, SQL语句
        * @param timeout_seconds, SQL语句执行超时时间, 默认超时时间为20s
        * @return `typing.List[typing.List[str]]`, 返回SQL语句执行结果, 如查询多条返回[['1', '2', '3'], ['a', 'b', 'c']], 查询单条或数据库操作记录数量返回[['1']]
        '''

        cmd = win32com.client.Dispatch(r"ADODB.Command")
        cmd.ActiveConnection = self.conn
        cmd.CommandText = sql
        cmd.CommandType = 1
        cmd.CommandTimeout = timeout_seconds
        cmd.Prepared = True
        rs, line_count = cmd.Execute()

        lines = []

        if rs.Fields.Count == 0:
            line = []
            line.append(str(line_count))
            lines.append(line)
        else:            
            while not rs.EOF:
                line = []
                for i in range(rs.Fields.Count):
                    line.append(str(rs.Fields.Item(i).Value))
                lines.append(line)
                rs.MoveNext()
            rs.Close()

        return lines

    def close(self) -> typing.NoReturn:
        '''
        关闭数据库连接
        '''

        self.conn.Close()