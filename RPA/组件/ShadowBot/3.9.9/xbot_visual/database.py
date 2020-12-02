from xbot import ado

from ._core import visual_action

@visual_action
def connect(**args):
    conn_str = args['conn_str']

    db = ado.Database()
    db.open(conn_str)

    return db

@visual_action
def exec(**args):
    connect_way = args['connect_way']
    sql = args['sql']
    timeout_seconds = args['timeout_seconds']

    db = None
    close_db = False
    if connect_way == 'database':
        db = args['database']
    if connect_way == 'conn_str':
        conn_str = args['conn_str']

        db = ado.Database()
        db.open(conn_str)
        close_db = True

    result = db.exec(sql, timeout_seconds)
    if close_db:
        db.close()

    return result

@visual_action
def close(**args):
    db = args['database']

    db.close()
