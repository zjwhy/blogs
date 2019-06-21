# 数据分析面试必备——SQL你准备好了吗？ 

2019-05-31 17:03

![img](http://5b0988e595225.cdn.sohucs.com/images/20190531/b1d8fceb4de543aa893b477a843cb46a.jpeg)

数据分析师的招聘JD你们一定不陌生：

![img](http://5b0988e595225.cdn.sohucs.com/images/20190531/82a3ad92e0f041df93ae59782d5098c8.jpeg)

可以说，**不是每个数据分析岗都要求python，但是每个数据分析岗都需要会SQL。**写这篇文章是希望帮助还没有实战过SQL的小伙伴、或者了解一些SQL语句，但是担心自己了解的太片面的小伙伴。

这篇文章主要介绍的是：如果想要面试数据分析岗位，最优先需要掌握的SQL技能是哪些呢？读完本文，你能快速知道：

1、除了select 这种基本的语句，我最应该马上掌握的SQL语句和知识是什么？

2、面试中SQL题80%都在考察的语法是什么？

3、这些语法应该怎么使用？

本文将从三大块介绍入门SQL需要掌握的语法和知识，分别是最基础的选择（select）和连接（join/union）；最常用的函数（distinct/group by/order by等）；一些小小的进阶技巧（组内排序、取前百分之多少的值、时间函数）。

![img](http://5b0988e595225.cdn.sohucs.com/images/20190531/d984bee0e5714378b2396d7c02ccba2d.png)

一、最基本（选数据）

![img](http://5b0988e595225.cdn.sohucs.com/images/20190531/cb3a5eddb3cc492bae24b0139d894945.gif)

•怎么把数据从表里选出来？

-- 从table_1中选择a这一列

```sql
select a from table_1
```

•想要的数据在多张表里，想取多个字段，该怎么办？—— 表连接

-- table_1中有id,age; table_2中有id，sex。想取出id,age,sex 三列信息

-- 将table_1,table_2 根据主键id连接起来

```SQL
select a.id,a.age,b.sex from

(select id,age from table_1) a --将select之后的内容存为临时表a

join

(select id, sex from table_2) b --将select之后的内容存为临时表b

on a.id =b.id
```

在这里先介绍一下几种join: （敲重点，很容易问的哦）

![img](http://5b0988e595225.cdn.sohucs.com/images/20190531/5b52afc4f9ab47ffb342c300c2c053ba.jpeg)

**join :**hive的join默认是inner join，找出左右都可匹配的记录；

![img](http://5b0988e595225.cdn.sohucs.com/images/20190531/5f3ea3178c13446c81f20281776ff63d.png)

**left join:** 左连接，以左表为准，逐条去右表找可匹配字段，如果有多条会逐次列出，如果没有找到则是NULL；

![img](http://5b0988e595225.cdn.sohucs.com/images/20190531/bb0c3c7c01494be2bf7150ece479f6c4.png)

**right join：**右连接，以右表为准，逐条去左表找可匹配字段，如果有多条会逐次列出，如果没有找到则是NULL；

![img](http://5b0988e595225.cdn.sohucs.com/images/20190531/8a053cf432e041bc9b5dce9403f9a5c8.png)

**full outer join:**全连接，包含两个表的连接结果，如果左表缺失或者右表缺失的数据会填充NULL。

![img](http://5b0988e595225.cdn.sohucs.com/images/20190531/b77ab202549b4e5fabfc704fc4b3ab1a.png)

每种join 都有on , on的是左表和右表中都有的字段。join 之前要确保关联键是否去重，是不是刻意保留非去重结果。

•两张表数据的字段一样，想合并起来，怎么办？

-- 不去重，合并两张表的数据

```SQL
select * from

(

select id from table_1

UNION ALL

select id from table_2

)t;
```

union和union all 均基于列合并多张表的数据，所合并的列格式必须完全一致。union的过程中会去重并降低效率，union all 直接追加数据。union 前后是两段select 语句而非结果集。

![img](http://5b0988e595225.cdn.sohucs.com/images/20190531/ce4e56cff12847999a88abc946dd90d1.png)

二、最常用

![img](http://5b0988e595225.cdn.sohucs.com/images/20190531/a9675efbac564c8b8105f32782f03966.gif)

（不是用这个就是用那个，更有可能多重组合）

为方便大家理解每个函数的作用，先建一个表，后面以这个为示例。

![img](http://5b0988e595225.cdn.sohucs.com/images/20190531/21122b02ca6e443180662729f74e3c68.jpeg)

•如果有千万用户数据，想知道有多少去重的用户数？—— 去重 distinct

-- 罗列不同的id

```SQL
select distinct id from table_1
```

-- 统计不同的id的个数

```SQL
select count(distinct id) from table_1
```

-- 优化版本的count distinct

```SQL
select count(*) from

(select distinct id from table_1) tb
```

distinct 会对结果集去重，对全部选择字段进行去重，并不能针对其中部分字段进行去重。使用count distinct进行去重统计会将reducer数量强制限定为1，而影响效率，因此适合改写为子查询。

•想分性别进行统计，看看男女各多少？—— 聚合函数和group by

-- 统计不同性别（F、M）中，不同的id个数

```SQL
select count(distinct id) from table_1

group by sex
```

-- 其它的聚合函数例如：max/min/avg/sum

-- 统计最大/最小/平均年龄

```SQL
select max(age), min(age),avg(age) from

table_1

group by id
```

聚合函数帮助我们进行基本的数据统计，例如计算最大值、最小值、平均值、总数、求和

•只想查看A公司的男女人数数据？—— 筛选 where/having

-- 统计A公司的男女人数

```SQL
select count(distinct id) from table_1

where company = 'A'

group by sex
```

-- 统计各公司的男性平均年龄，并且仅保留平均年龄30岁以上的公司

```SQL
select company, avg(age) from table_1

where sex = 'M'

group by company

having avg(age)>30;
```

•希望查询结果从高到低/从低到高排序？—— 排序 order by

-- 按年龄全局倒序排序取最年迈的10个人

```SQL
select id,age from table_1 order by age DESC

limit 10
```

•将数值型的变量转化为分类型的变量？ —— case when 条件函数

-- 收入区间分组

```SQL
select id,

(case when CAST(salary as float)<50000 Then '0-5万'

when CAST(salary as float)>=50000 and CAST(salary as float)<100000 then '5-10万'

when CAST(salary as float) >=100000 and CAST(salary as float)<200000 then '10-20万'

when CAST(salary as float)>200000 then '20万以上'

else NULL end

from table_1;
```

case 函数的格式为（case when 条件1 then value1 else null end）, 其中else 可以省，但是end不可以省。

在这个例子里也穿插了一个CAST的用法，它常用于string/int/double型的转换。

•字符串

1.concat( A, B...)返回将A和B按顺序连接在一起的字符串，如：concat('foo', 'bar') 返回'foobar'

```SQL
select concat('www','.iteblog','.com') from

iteblog;
```

--得到 www.iteblog.com

\2. split(str, regex)用于将string类型数据按regex提取，分隔后转换为array。

-- 以","为分隔符分割字符串，并转化为array

```SQL
Select split("1,2,3",",")as value_array from table_1;
```

-- 结合array index,将原始字符串分割为3列

```SQL
select value_array[0],value_array[1],value_array[2] from

(select split("1,2,3",",")as value_array from table_1 )t
```

\3. substr（str,0,len) 截取字符串从0位开始的长度为len个字符。

```SQL
select substr('abcde',3,2) from

iteblog;
```

-- 得到cd

三、基础进阶

•不想全局排序，需要分组排序？—— row_number(）

-- 按照字段salary倒序编号

```SQL
select *, row_number() over (order by salary desc) as row_num from table_1;
```

-- 按照字段deptid分组后再按照salary倒序编号

```SQL
select *, row_number() over (partition by deptid order by salary desc) as rank from table_1;
```

![img](http://5b0988e595225.cdn.sohucs.com/images/20190531/ff8fc067e9f7481cb5e1a8ae84df62f4.jpeg)

按照depid分组，对salary进行排序（倒序）

除了row_number函数之外，还有两个分组排序函数，分别是rank() 和dense_rank()。

rank()排序相同时会重复，总数不会变 ，意思是会出现1、1、3这样的排序结果；

dense_rank() 排序相同时会重复，总数会减少，意思是会出现1、1、2这样的排序结果。

row_number() 则在排序相同时不重复，会根据顺序排序。

•想要获取top10%的值？—— percentile 百分位函数

-- 获取income字段的top10%的阈值

```SQL
select percentile(CAST (salary AS int),0.9)) as income_top10p_threshold from table_1;
```

-- 获取income字段的10个百分位点

```SQL
select percentile(CAST (salary AS int),array(0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0)) as income_percentiles

from table_1;
```

•想要对时间字段进行操作？—— 时间函数

-- 转换为时间数据的格式

```SQL
select to_date("1970-01-01 00:00:00") as start_time from table_1;
```

-- 计算数据到当前时间的天数差

```SQL
select datediff('2016-12-30','2016-12-29');
```

-- 得到 "1"

to_date函数可以把时间的字符串形式转化为时间类型，再进行后续的计算；

常用的日期提取函数包括：

year()/month()/day()/hour()/minute()/second()

日期运算函数包括datediff(enddate,stratdate) 计算两个时间的时间差（day)；

date_sub(stratdate,days) 返回开始日期startdate减少days天后的日期。

date_add(startdate,days) 返回开始日期startdate增加days天后的日期。

四、常见笔试/面试题

**例：有3个表S，C，SC：**

S（SNO，SNAME）代表（学号，姓名）

C（CNO，CNAME，CTEACHER）代表（课号，课名，教师）

SC（SNO，CNO，SCGRADE）代表（学号，课号，成绩）

**问题：**

1，找出没选过“黎明”老师的所有学生姓名。

2，列出2门以上（含2门）不及格学生姓名及平均成绩。

3，既学过1号课程又学过2号课所有学生的姓名。

\1. -- 考察条件筛选

```SQL
select sname from s where sno not in

( select sno from sc where cno in

(

select distinct cno from c where cteacher='黎明'

)

);
```

\2. -- 考察聚合函数，条件筛选

```SQL
select s.sname, avg_grade from s

join

(select sno from sc where scgrade < 60 group by sno having count(*) >= 2) t1

on s.sno = t1.sno

join

(select sno, avg(scgrade) as avg_grade from sc group by sno ) t2

on s.sno = t2.sno;
```

\3. -- 考察筛选、连接

```SQL
select sname from

( select sno from sc where cno = 1) a

join

(select sno from sc where cno = 2) b

on a.sno = b.sno
```

这篇SQL面试和笔试的入门文章，主旨是快速、清晰的把握重点。希望大家都能快快入门SQL~



[转载连接](<http://www.sohu.com/a/317830995_99914128>)