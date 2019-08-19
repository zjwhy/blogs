[TOC]

# Mysql5.7 GROUP BY 报错

把sql_mode 改成非only_full_group_by模式。验证是否生效 SELECT @@GLOBAL.sql_mode 或 SELECT @@sql_mode



```mysql
SET sql_mode ='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
```

## group by 提示警告问题

## 警告信息

```mysql
com.MySQL.jdbc.exceptions.jdbc4.MySQLSyntaxErrorException: Expression #2 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'col_user_6.a.START_TIME' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
```

## 原因：

​	sql_mode 默认设置了 ‘ONLY_FULL_GROUP_BY’

查询时为严谨模式，除了group by字段以外的字段无法查询

## 查询sql_mode 

```
select @@global.sql_mode
```

结果：

```
'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'
```

## 解决方案一

​	更改sql_model 方式 去掉ONLY_FULL_GROUP_BY 即可

```mysql
set @@global ='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'
```

重启数据库. windows 没有重启命令直接关闭数据库重启即可

```
net stop mysql
net start mysql
```

**set @global.sql_mode只对新建的库生效，对已经建好的库可以使用 set @sql_mode**

该方案的弊端是 数据库重启还是会回复到默认sql_mode。。。

## 解决方案二

修改配置文件 mysql数据库安装路径下的my.ini

```mysql
[mysqld]
sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'
```

如果my.ini 中已经有了sql_mode，只需将 ‘ONLY_FULL_GROUP_BY’删掉即可。该项配置一定要是在[mysqld]下

重启数据库. windows 没有重启命令直接关闭数据库重启即可

```
net stop mysql
net start mysql
```

## 坑

1、此次我使用的是win7系统，数据库采用的压缩包安装，my.ini文件是自己建立的，我已经开启了后缀名显示，但是win7系统默认勾选了 对已知文件类型隐藏后缀名，新建的my.ini 一定要看一下他的属性是不是my.ini  还是my.ini.txt