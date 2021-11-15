# selenium接管方式

1、指定启动参数打开浏览器

```
# 指定chrome 远程调试接口与用户目录
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"
```

2selenium接管

```python
self.options = webdriver.ChromeOptions()
self.options.add_experimental_option("debuggerAddress", "127.0.1:9222")
self.chromeDriver = webdriver.Chrome(driverPath, options=self.options)
```



# chrome远程调试原理分析（CDP协议）

## 参考链接

https://chromedevtools.github.io/devtools-protocol/

https://chromedevtools.github.io/devtools-protocol/

https://ceshiren.com/t/topic/3567

https://www.daimajiaoliu.com/daima/4eee866b8900402

### 协议

webdriver协议

### 使用 DevTools 作为协议客户端

开发者工具前端可以附加到远程运行的 Chrome 实例进行调试。要使此方案正常运行，您应该使用 remote-debugging-port 命令行开关启动您的*主机*Chrome 实例

```
chrome.exe --remote-debugging-port=9222
```

然后，您可以使用不同的用户配置文件启动一个单独的*客户端*Chrome 实例：

```
chrome.exe --user-data-dir=<某个目录>
```

现在，您可以从*客户端*导航到给定端口并附加到任何发现的选项卡以进行调试：[http://localhost:9222](http://localhost:9222/)

### 监听协议

这对于理解 DevTools 前端如何使用协议特别方便。您可以在发生时查看所有请求/响应和方法。

[![协议监视器的屏幕截图](https://chromedevtools.github.io/devtools-protocol/images/protocol-monitor.png)](https://chromedevtools.github.io/devtools-protocol/images/protocol-monitor.png)

单击 DevTools 右上角的齿轮图标以打开*设置*面板。选择设置左侧的*实验*。打开“Protocol Monitor”，然后关闭并重新打开 DevTools。现在单击 ⋮ 菜单图标，选择*更多工具*，然后选择*协议监视器*。

您还可以使用协议监视器（版本 92.0.4497.0+）发出您自己的命令。如果该命令不需要任何参数，请在“协议监视器”面板底部的提示中键入该命令，然后按 Enter，例如， `Page.captureScreenshot`。如果命令需要参数，请将它们作为 JSON 提供，例如 `{"command":"Page.captureScreenshot","parameters":{"format": "jpeg"}}`.

# http获取启动信息

#### GET `/json/version`

Browser version metadata

```
{
    "Browser": "Chrome/72.0.3601.0",
    "Protocol-Version": "1.3",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3601.0 Safari/537.36",
    "V8-Version": "7.2.233",
    "WebKit-Version": "537.36 (@cfede9db1d154de0468cb0538479f34c0755a0f4)",
    "webSocketDebuggerUrl": "ws://localhost:9222/devtools/browser/b0b8a4fb-bb17-4359-9533-a8d9f3908bd8"
}
```

#### GET `/json` or `/json/list`

A list of all available websocket targets.

```
[ {
  "description": "",
  "devtoolsFrontendUrl": "/devtools/inspector.html?ws=localhost:9222/devtools/page/DAB7FB6187B554E10B0BD18821265734",
  "id": "DAB7FB6187B554E10B0BD18821265734",
  "title": "Yahoo",
  "type": "page",
  "url": "https://www.yahoo.com/",
  "webSocketDebuggerUrl": "ws://localhost:9222/devtools/page/DAB7FB6187B554E10B0BD18821265734"
} ]
```

#### GET `/json/protocol/`

The current devtools protocol, as JSON:

```
{
  "domains": [
      {
          "domain": "Accessibility",
          "experimental": true,
          "dependencies": [
              "DOM"
          ],
          "types": [
              {
                  "id": "AXValueType",
                  "description": "Enum of possible property types.",
                  "type": "string",
                  "enum": [
                      "boolean",
                      "tristate",
// ...
```

#### GET `/json/new?{url}`

Opens a new tab. Responds with the websocket target data for the new tab.

#### GET `/json/activate/{targetId}`

Brings a page into the foreground (activate a tab).

For valid targets, the response is 200: `"Target activated"`. If the target is invalid, the response is 404: `"No such target id: {targetId}"`

#### GET `/json/close/{targetId}`

Closes the target page identified by `targetId`.

For valid targets, the response is 200: `"Target is closing"`. If the target is invalid, the response is 404: `"No such target id: {targetId}"`

#### WebSocket `/devtools/page/{targetId}`

The WebSocket endpoint for the protocol.

#### GET `/devtools/inspector.html`

A copy of the DevTools frontend that ship with Chrome.

# 远程调试步骤

1、设置远程调试端口

```
chrome.exe --remote-debugging-port=9222
```

2、http获取浏览信息

```
postman    http://localhost:9222/json/version
```

```
{
    "Browser": "Chrome/91.0.4472.124",
    "Protocol-Version": "1.3",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "V8-Version": "9.1.269.36",
    "WebKit-Version": "537.36 (@7345a6d1bfcaff81162a957e9b7d52649fe2ac38)",
    "webSocketDebuggerUrl": "ws://localhost:9222/devtools/browser/325848c7-f588-4b2a-8d53-871d0c407498"
}
```

3、ws执行后续命令示例

```
# 获取sessionid

import websocket
import json
ws = websocket.create_connection("ws://localhost:9222/devtools/browser/325848c7-f588-4b2a-8d53-871d0c407498")
cmd = {"id": 100, "method": "Target.attachToTarget", "params": {"targetId":"C6D11457622705623B8F5381612D197D", "flatten":True}}
data = json.dumps(cmd, ensure_ascii=False)
ws.send(data)
while 1:
    result = ws.recv()
    print(result)

```

4、event示例

```
import websocket
import json
ws = websocket.create_connection("ws://localhost:9222/devtools/page/7064B86A54979CA238AABB1784858038")
cmd = {"id": 1, "method": "Page.enable", "params": {"windowId": 1, "bounds":{

}}}
data = json.dumps(cmd, ensure_ascii=False)
ws.send(data)
while 1:
    result = ws.recv()
    print(result)
```

```
E:\Desktop\RPAWork\CBSEditor\branches\develop_v3.0\RpaStudioPublish\public\python\python.exe E:/Desktop/RPAWork/CSEditorPython/trunk/compentsAdministration/2.py
{"id":1,"result":{}}
{"method":"Page.frameStartedLoading","params":{"frameId":"7064B86A54979CA238AABB1784858038"}}
{"method":"Page.frameDetached","params":{"frameId":"A099BBAD2608A370D9C76CA5479B5621","reason":"remove"}}
{"method":"Page.frameNavigated","params":{"frame":{"id":"7064B86A54979CA238AABB1784858038","loaderId":"95332EA5BBB3B9346ED939DB007F59D0","url":"https://fanyi.baidu.com/","urlFragment":"#en/zh/Types","domainAndRegistry":"baidu.com","securityOrigin":"https://fanyi.baidu.com","mimeType":"text/html","adFrameType":"none","secureContextType":"Secure","crossOriginIsolatedContextType":"NotIsolated","gatedAPIFeatures":["SharedArrayBuffersTransferAllowed"]}}}
{"method":"Page.frameAttached","params":{"frameId":"CAC1E51A034347E0CD90FAC57B040682","parentFrameId":"7064B86A54979CA238AABB1784858038"}}
{"method":"Page.frameStartedLoading","params":{"frameId":"CAC1E51A034347E0CD90FAC57B040682"}}
{"method":"Page.frameNavigated","params":{"frame":{"id":"CAC1E51A034347E0CD90FAC57B040682","parentId":"7064B86A54979CA238AABB1784858038","loaderId":"62CC3D0059086BA4A88DB784C824BFD6","name":"doc-view-iframe","url":"about:blank","domainAndRegistry":"","securityOrigin":"://","mimeType":"text/html","adFrameType":"none","secureContextType":"Secure","crossOriginIsolatedContextType":"NotIsolated","gatedAPIFeatures":["SharedArrayBuffersTransferAllowed"]}}}
{"method":"Page.frameStoppedLoading","params":{"frameId":"CAC1E51A034347E0CD90FAC57B040682"}}
{"method":"Page.domContentEventFired","params":{"timestamp":873617.921655}}
{"method":"Page.frameAttached","params":{"frameId":"E4F8EB74C7D088A7D98D9F2B6C02F25C","parentFrameId":"7064B86A54979CA238AABB1784858038","stack":{"callFrames":[{"functionName":"qL","scriptId":"280","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2008-s.js","lineNumber":0,"columnNumber":89227},{"functionName":"cf","scriptId":"280","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2008-s.js","lineNumber":0,"columnNumber":108246},{"functionName":"yk","scriptId":"280","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2008-s.js","lineNumber":0,"columnNumber":108414},{"functionName":"ck","scriptId":"280","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2008-s.js","lineNumber":0,"columnNumber":128015},{"functionName":"GZ.<computed>.<computed>","scriptId":"280","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2008-s.js","lineNumber":0,"columnNumber":128242},{"functionName":"N5","scriptId":"280","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2008-s.js","lineNumber":0,"columnNumber":138720},{"functionName":"y","scriptId":"280","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2008-s.js","lineNumber":0,"columnNumber":39001},{"functionName":"","scriptId":"280","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2008-s.js","lineNumber":0,"columnNumber":138980},{"functionName":"_iwWM","scriptId":"280","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2008-s.js","lineNumber":0,"columnNumber":138987},{"functionName":"","scriptId":"280","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2008-s.js","lineNumber":0,"columnNumber":138992}]}}}
{"method":"Page.frameStartedLoading","params":{"frameId":"E4F8EB74C7D088A7D98D9F2B6C02F25C"}}
{"method":"Page.frameStoppedLoading","params":{"frameId":"E4F8EB74C7D088A7D98D9F2B6C02F25C"}}
{"method":"Page.frameDetached","params":{"frameId":"E4F8EB74C7D088A7D98D9F2B6C02F25C","reason":"remove"}}
{"method":"Page.frameAttached","params":{"frameId":"A85725E42A62F74C9D8873D8F81AD2BA","parentFrameId":"7064B86A54979CA238AABB1784858038","stack":{"callFrames":[{"functionName":"ix","scriptId":"318","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2060-s.js?v=0.14359652757150543","lineNumber":1,"columnNumber":62835},{"functionName":"aY","scriptId":"318","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2060-s.js?v=0.14359652757150543","lineNumber":1,"columnNumber":100587},{"functionName":"","scriptId":"318","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2060-s.js?v=0.14359652757150543","lineNumber":1,"columnNumber":101855},{"functionName":"xx.<computed>","scriptId":"318","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2060-s.js?v=0.14359652757150543","lineNumber":1,"columnNumber":109310},{"functionName":"v1","scriptId":"318","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2060-s.js?v=0.14359652757150543","lineNumber":1,"columnNumber":101811},{"functionName":"vW","scriptId":"318","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2060-s.js?v=0.14359652757150543","lineNumber":1,"columnNumber":102541},{"functionName":"p","scriptId":"318","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2060-s.js?v=0.14359652757150543","lineNumber":1,"columnNumber":144953},{"functionName":"Me.<computed>.<computed>","scriptId":"318","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2060-s.js?v=0.14359652757150543","lineNumber":1,"columnNumber":145288},{"functionName":"PN","scriptId":"318","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2060-s.js?v=0.14359652757150543","lineNumber":1,"columnNumber":147945},{"functionName":"D","scriptId":"318","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2060-s.js?v=0.14359652757150543","lineNumber":1,"columnNumber":41294},{"functionName":"","scriptId":"318","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2060-s.js?v=0.14359652757150543","lineNumber":1,"columnNumber":148232},{"functionName":"_3Ku4","scriptId":"318","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2060-s.js?v=0.14359652757150543","lineNumber":1,"columnNumber":148242},{"functionName":"","scriptId":"318","url":"https://dlswbr.baidu.com/heicha/mw/abclite-2060-s.js?v=0.14359652757150543","lineNumber":1,"columnNumber":148247}]}}}
{"method":"Page.frameStartedLoading","params":{"frameId":"A85725E42A62F74C9D8873D8F81AD2BA"}}
{"method":"Page.frameStoppedLoading","params":{"frameId":"A85725E42A62F74C9D8873D8F81AD2BA"}}
{"method":"Page.frameDetached","params":{"frameId":"A85725E42A62F74C9D8873D8F81AD2BA","reason":"remove"}}
{"method":"Page.loadEventFired","params":{"timestamp":873623.526458}}
{"method":"Page.frameStoppedLoading","params":{"frameId":"7064B86A54979CA238AABB1784858038"}}
```

