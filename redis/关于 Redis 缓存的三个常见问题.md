## 关于 Redis 缓存的三个一定要知道的问题哟！

- 缓存穿透

- - 缓存空对象
    - 布隆过滤器

- 缓存击穿

- 缓存雪崩

[![img](https://mmbiz.qpic.cn/mmbiz_jpg/JdLkEI9sZffUstrsicqnPMIoP91TTibMu8vKh5u8C2LGDvKMqmU6ACibb7XP2lwXwVHsYyMoibBp13p0ysicf6N3wzA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)](https://mp.weixin.qq.com/s?__biz=MzUzMTA2NTU2Ng==&mid=2247487551&idx=1&sn=18f64ba49f3f0f9d8be9d1fdef8857d9&chksm=fa496f8ecd3ee698f4954c00efb80fe955ec9198fff3ef4011e331aa37f55a6a17bc8c0335a8&scene=21#wechat_redirect)

**二哈最近都没看Redis，现在回来温习下，现在从Redis的三大缓存开始重新探一探有多深有多浅（\* ^▽^ \*）**

![img](https://mmbiz.qpic.cn/mmbiz_png/JdLkEI9sZffUstrsicqnPMIoP91TTibMu83nbZBrxIaKqMkU8ygcqwyiaW0TSbQopbH4qqTBp8G8ycfy5xuBXUdJg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)img

让我来开始知识的醍醐灌顶把！是时候表演真正的技术了。（哔哔哔哔....）

![img](https://mmbiz.qpic.cn/mmbiz_png/JdLkEI9sZffUstrsicqnPMIoP91TTibMu8JM1xR1qHHMzJVtOJ34jcoxmMZcEtibQwibmswTdYWMhhIIpcvBoA42ew/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)img

**铁子们，看在二哈这么卖力的份上，如果觉得这里对你有帮助的话，请动动你的小手，比个❥（^ _-）爱心推荐哟。**

接下来就开始我们的Redis的三大缓存问题之旅，让我们坐在上二哈的小飞船游一游这圣女峰。

![img](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)img

在Redis缓存中有三个必须要知道概念：**缓存穿透，缓存击穿和缓存雪崩。**

# 缓存穿透

那什么是缓存穿透，它就是指当用户在查询一条数据的时候，而此时数据库和缓存却没有关于这条数据的任何记录，而这条数据在缓存中没找到就会向数据库请求获取数据。它拿不到数据时，是会一直查询数据库，这样重组数据库的访问造成很大的压力。

如：用户查询一个id = -1的商品信息，一般数据库id值都是从1开始自增，很明显这条信息是不在数据库中，当没有信息返回时，会一直向数据库查询，给当前数据库的造成很大的访问压力。

这时候我们要想一想，该如何解决这个问题呢？o（╥﹏╥）o

一般我们可以想到从缓存开始出发，想如果我们给缓存设置一个如果当前数据库不存在的信息，把它缓存成一个空对象，返回给用户。

^ _ ^没错，这是一个解决方案，也就是我们常说的缓存空对象（代码维护简单，但是效果不是很好）。

Redis也为我们提供了一种解决方案，那就是布隆过滤器（代码维护比较复杂，效果挺好的）。

**那接下来，二哈先解释下这两种方案：**

## 缓存空对象

那什么是缓存空对象呀，二哈！别急，缓存空对象它就是指一个请求发送过来，如果此时缓存中和数据库都不存在这个请求所要查询的相关信息，那么数据库就会返回一个空对象，变成这个空对象和请求关联起来存到缓存中，当下次还是这个请求过来的时候，这时缓存就会命中，就直接从缓存中返回这个空对象，这样可以减少访问数据库的压力，提高当前数据库的访问性能。我们接下来可以看下面这个流程呀〜

![img](https://mmbiz.qpic.cn/mmbiz_png/JdLkEI9sZffUstrsicqnPMIoP91TTibMu8eHAvXmfNGjStv6PHX6hBaFfqEfsvUa6Af1JaH7CzZia58hX4d17Fp4Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)img

这时候，我们就会问了呀〜，如果大量不存在的请求过来，那么这时候缓存岂不是会缓存很多空对象了吗~~~

没错哦！这也是使用缓存空对象会导致一个问题：如果时间一长这样会导致缓存中存在大量空对象，这样交替会占用很多的内存空间，还会浪费很多资源呀！。那这有没有什么可以解决的方法呢？我们来想一想：我们可以将这些对象在重启之后清理下不久可以了吗〜

嗯嗯，没错！在想想Redis里是不是给我们提供了有关过期时间的命令呀（*^▽^*），这样我们可以在设置空对象的时间，顺便设置一个过期时间，就可以解决个问题了呀！

```
setex key seconds valule:设置键值对的同时指定过期时间(s)
```

在Java中直接调用API操作即可：

```
redisCache.put(Integer.toString(id), null, 60) //过期时间为 60s
```

## 布隆过滤器

那布隆过滤器是不是不是一个过滤器，过滤东西的呀！哎呀，你太聪明了，没错它就是用来过滤东西的，它是一种基于概率的数据结构，主要使用爱判断当前某人一个元素是否在该集合中，运行速度快。我们也可以简单理解为是一个不怎么精确的set结构（set具有去重的效果）。但是有个小问题是：当你使用它的contains方法去实际上布隆过滤器不是特别不精确，但是只要参数设置的合理，它的精确度可以控制的相对足够精确，只会有小小的误判概率（这是可以接受的呀〜）。当布隆过滤器说某个值存在时，这个值可能不存在；当它说不存在时，那就肯定不存在。

**这里有个典型的例子呀，来自钱大：**

打个比方，当它说不认识你时，肯定就不认识；当它说见过你时，可能根本就没见过面，不过因为你的脸跟它认识的人中某脸比较相似（某人些熟脸的系数组合），所以误判以前见过你。在上面的使用场景中，布隆过滤器能准确过滤掉那些已经看过的内容，那些没有看过的新内容，它也会过滤掉极小部分（误判），但是大部分新内容它都能正确识别。这样就可以完全保证推荐给用户的内容都是无重复的。

**说了这么久，那布隆过滤器到底有什么特点呢：**

特色吗，多多来让一个个跟你吹吹（吹到你怀疑人生（≧∇≦）ﾉ）

1. 一个非常大的二进制位数发行（发行中只存在0和1）
2. 拥有多个个哈希函数（哈希函数）
3. 在空间效率和查询效率都非常高
4. 布隆过滤器不会提供删除方法，在代码维护上比较困难。

每个布隆过滤器对应到Redis的数据结构里面就是一个大型的位置数组和几个不一样的无偏hash函数。所谓无偏就是能够把元素的hash值算得比较均匀。

![img](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)img

向布隆过滤器中添加key时，会使用多个hash函数对key进行hash算得一个整体索引值然后对位长度进行取模运算得到一个位置，每个hash函数都会算得一个不同的位置。再（每一个键都通过一些的hash函数映射到一个巨大的位置上，映射成功后，会在把位置上对应的位置改成）为1。）

**那为什么布隆过滤器会存在误判率呢？**

误判吗？人生哪有不摔跤，只要锄头挥得好，照样能挖到。（咳嗽咳，说偏了...）

其实它会误判是如下这个情况：

![img](https://mmbiz.qpic.cn/mmbiz_png/JdLkEI9sZffUstrsicqnPMIoP91TTibMu8F53yX2s4VdjQGK1BepYkv72Odv5o0fuQUZ6dsL4DPh7Vpaiapv5uHwA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)img

当key1和key2映射到位上方的位置为1时，假设这时候来了个key3，要查询是不是在里面，恰好key3对应位置也映射到了这之间，那么布隆过滤器会认为它是存在的，这时候就会产生误判（因为明明key3是不在的）。

O（∩_∩）O哈哈〜，这时候你会问了：如何提高布隆过滤器的准确率呢？

**要提高布隆过滤器的准确率，就要说到影响它的三个重要因素：**

1. 哈希函数的好坏
2. 存储空间大小
3. 哈希函数个数

hash函数的设计也是一个十分重要的问题，对于好的哈希函数能大大降低布隆过滤器的误判率。

（这就好比优秀的配件之所以能够运行这么顺畅就在于其内部设计的得当。）

同时，对于一个布隆过滤器来说，如果它的位置重叠尺寸的话，那么每个键通过hash函数映射的位置会变得稀疏很多，不会那么微小，有利于提高布隆过滤器的准确率。同时，对于一个布隆过滤器来说，如果键通过许多哈希函数映射，那么在位上上就会有很多位置有标志，这样当用户查询的时候，在通过布隆过滤器来找的时候，误判率也会相应降低。

对于其内部原理，有兴趣的同学可以看看关于布隆过滤的数学知识，里面有关于它的设计算法和数学知识。（其实也挺简单〜）

# 缓存击穿

缓存击穿是指有某个键经常被查询，经常被用户特殊关怀，用户非常love它（*^▽^*），也就类比“熟客”或一个键经常不被访问。但是这时候，如果这个键在缓存的过期时间失效的时候或者这是个冷门键时，这时候突然有大量有关这个键的访问请求，这样会导致大并发请求直接穿透缓存，请求数据库，瞬间对数据库的访问压力增大。

**归纳起来：造成缓存击穿的原因有两个。**

（1）一个“冷门”键，突然被大量用户请求访问。

（2）一个“热门”键，在缓存中时间恰好过期，这时有大量用户来进行访问。

![img](https://mmbiz.qpic.cn/mmbiz_png/JdLkEI9sZffUstrsicqnPMIoP91TTibMu8ejD70HGVScjZCCWKzYbMuBiaeyAGiabiatFfuLRBnKZicTnITDakO9cP5A/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)img

对于缓存击穿的问题：我们常用的解决方案是加锁。对于密钥过期的时候，当密钥要查询数据库的时候加上一把锁，这时只能让第一个请求进行查询数据库，然后把从数据库中查询到的值存储到缓存中，对于其余的相同的键，可以直接从缓存中获取即可。

如果我们是在单机环境下：直接使用常用的锁即可（如：Lock，Synchronized等），在分布式环境下我们可以使用分布式锁，如：基于数据库，基于Redis或者zookeeper的分布式锁。

![img](https://mmbiz.qpic.cn/mmbiz_png/JdLkEI9sZffUstrsicqnPMIoP91TTibMu82hrRxRF794S19MWt9GbvMSyQJrB8iaM0ggV6iczyia61ZeY6f0jCayH4Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)img

# 缓存雪崩

缓存雪崩是指在某人一个时间段内，缓存集中过期失效，如果这个时间段内有大量请求，而查询数据量巨大，所有的请求都会达到存储层，存储层的调用量会暴增，引起数据库压力过大甚至停机机。

**原因：**

1. Redis突然停机机
2. 大部分数据错误

**举个例子理解下吧：**

例如我们基本上都经历过购物狂欢节，假设商家聚会23：00-24：00商品打骨折促销活动。程序小哥哥在设计的时候，在23:00把商家打骨折的商品放到缓存中，并通过redis的expire设置了过期时间为1小时。这个时间段许多用户访问这些商品信息，购买等等。但是刚好到了24:00点的时候，恰好还有很多用户在访问这些商品，这时候对这些商品的访问都会落到数据库上，导致数据库要抗住巨大的压力，稍有不慎会导致，数据库直接停机机（over）。

**当商品没有失效的时候是这样的：**

![img](https://mmbiz.qpic.cn/mmbiz_png/JdLkEI9sZffUstrsicqnPMIoP91TTibMu8tRHD97GeSQNiaPHyJIgO4GNh0uzF178PjgR6B5p45SNAc0lwVWvibNBg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)img

**当缓存GG（失效）的时候却是这样的：**

![img](https://mmbiz.qpic.cn/mmbiz_png/JdLkEI9sZffUstrsicqnPMIoP91TTibMu8jeB0dxD5DcjqFnbYzm3TVf7OCTCaYQdicEFDIBCZAAucVvsY6ibfdfrg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)img

**对于缓存雪崩有以下解决方案：**

**（1）redis高可用**

redis有可能挂掉，多增加几台redis实例，（一主多从或者多主多从），这样一台挂掉之后其他的还可以继续工作，其实就是建造的。

**（2）限流降级**

在缓存无效后，通过加锁或者通过堆栈来控制读数据库写缓存的线程数量，对某个键只允许一个线程查询数据和写缓存，其他线程等待。

**（3）数据预热**

数据加热的意味着就是在正式部署之前，我先把可能的数据先预先访问一遍，这样部分可能大量访问的数据就会加载到缓存中。在即将发生的大并发访问前手动触发加载缓存不同的键。

**（4）不同的过期时间**

设置不同的过期时间，让缓存重复的时间点正确均匀。