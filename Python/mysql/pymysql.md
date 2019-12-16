# 安装

```
pip install pymysql
```

# 使用代码

```python
import pymysql
#连接mysql
conn = pymysql.connect(
	host = '地址',
	user = '用户'，
	database = '数据库'，
	charset = 'utf-8'
)
#创建游标
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
# 可选参数 cursor 执行sql语句是返回字典
sql = ‘’
cursor.execute(sql)
cursor.close() #关闭游标
conn.close()  #关闭数据库连接
```

# 插入数据

```python
import pymysql
 
# 建立连接
conn = pymysql.connect(
    host="192.168.0.103",
    port=3306,
    user="root",
    password="123",
    database="xing",
    charset="utf8"
)
# 获取一个光标
cursor = conn.cursor()
# 定义将要执行的SQL语句
sql = "insert into userinfo (user, pwd) values (%s, %s);"
name = "wuli"
pwd = "123456789"
# 并执行SQL语句
cursor.execute(sql, [name, pwd]) #插入一条数据
# 涉及写操作注意要提交
conn.commit()
# 关闭连接
 
# 获取最新的那一条数据的ID
last_id = cursor.lastrowid
print("最后一条数据的ID是:", last_id)
 
cursor.close()
conn.close()
```

## cursor.execute和cursor.executemany

execute（） 插入单条数据

参数可以使用%s 或者format做占位符

```python
sql = 'update table set a=%s;
cursor.execute(sql %name)
db.commit


sql = 'udpate table set a={0}'
cursor.execut(sql.format(name))
```

executemany()

参数：

第一个是sql语句，

第二个是二维元祖或二维列表









