# 安装

```
wget -q -O - https://www.charlesproxy.com/packages/apt/PublicKey | sudo apt-key add -

sudo sh -c 'echo deb https://www.charlesproxy.com/packages/apt/ charles-proxy main > /etc/apt/sources.list.d/charles.list'

sudo apt-get update

sudo apt-get install charles-proxy
```

# 注册

help>Registered

```
Registered Name: https://zhile.io
License Key: 48891cf209c6d32bf4
```

# 保存证书

菜单Help->SSL Proxying->Save Charles Root Certificate…

证书命名为 CharlesRoot.cer 类型选择cer

```
openssl x509 -inform der -in CharlesRoot.cer -outform pem -out CharlesRoot.crt
```

# 安装证书

```
sudo cp CharlesRoot.crt /usr/share/ca-certificates

sudo dpkg-reconfigure ca-certificates //选择ask,勾选CharlesRoot.crt并确认
```

# 开拓期http代理

```
运行charles软件，菜单Proxy->Proxy Setting->标签Proxies下勾选Enable transparent HTTP proxying
至此，服务端配置结束
```

# 设置抓取https

、

```
在Charles中Proxy -> SSL Proxy Settings -> SSL Proxy中设置一个Host为*,Port为443的Location，主要是用来代理所有的HTTPS请求；
```



# 安卓抓包

1、 配置代理

2、 下载证书

浏览器中输入 [chls.pro/ssl](http://chls.pro/ssl) 来安装证书

到系统设置->安全->从设备内在或sd卡安装证书来安装

# 抓包

在charles软件中Proxy –> Start Recording
ps.抓到的请求域名下面的具体请求都显示为`<unknown>`,解决办法为：
在对应的域名上，鼠标右键选择`Enable SSL Proxying`即可



# 问题

-   无法抓取chrome

chrome安装SwitchyOmega插件，浏览器中用SwitchyOmega切换至设置的charlse 8888端口的代理，地址设置127.0。0.1



**参考内容**

*   https://blog.csdn.net/moqsien/article/details/79753343
*   https://blog.csdn.net/huuinn/article/details/82762952
*   https://blog.csdn.net/time_future/article/details/82935375