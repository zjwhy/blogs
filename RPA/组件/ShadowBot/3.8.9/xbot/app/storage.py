'''
数据存取模块
'''
from xbot._core import robot
from xbot._core.validation import valid, valid_multi, ValidPattern
import hashlib

def write(key, content):
    """
    持久化保存
    * @param key, 读取Key
    * @param content, 数据内容
    """
    if len(content) > 20000:
        raise ValueError("数据内容 长度超过20000个字符")

    robot.execute(f'Storage.Write', {'key' : _md5(str(key)), 'content' : str(content)})

def read(key) -> str:
    """
    读取持久化数据
    * @param storage_kind, 存储位置
    * @param key, 文本读取Key
    """
    return robot.execute(f'Storage.Read',{'key' : _md5(str(key))})

def _md5(key) -> str:
    md5 = hashlib.md5()
    md5.update(key.encode('utf-8'))
    return md5.hexdigest()


