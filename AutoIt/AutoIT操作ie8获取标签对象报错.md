# 背景

最近在做一个进项税认证的demo，像这种软件仅支持ie浏览器，更为夸张的是有的页面是针对ie8的xml。

在autoit写代码的时候都习惯这样写

```c
local $oIE = _IECreate(url)
$oIE.document.qeruySelector('#id')
```

但是有的页面仅支持ie8， 在控制台执行document.querySelector(‘#id’)时，返回的是一个[object Object]

而不是像普通标签一样的对象。

在执行上面AutoIt的代码时，会报错。导致继续无法操作

# 原因

ie8仅支持部分document API功能 ，不支持querySelector()

我们改为

```
$oIE.document.getElementById('id') 
$oIE.document.getElementByName('name') 
```

改为这样就可以了

具体支持哪些API还需要在ie控制台测试。