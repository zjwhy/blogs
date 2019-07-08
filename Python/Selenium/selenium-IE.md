# 驱动

[ie驱动下载地址](http://selenium-release.storage.googleapis.com/index.html)  可能需翻墙

[这个地址跳转过去可以访问](https://www.cnblogs.com/misswjr/p/9453566.html)

我是ie11 采用3.0

# 使用前注意事项

- 环境变量设置，或者再接再程序中输入驱动路径

- inter选项配置

  1、取消所有勾选的保护模式
  
  ![internet选项-安全](https://img-blog.csdn.net/20160330091216539)
  
  2、高级选项里取消勾选 启用增强保护模式。
  
  ​	![internet选项-高级](https://img-blog.csdn.net/20160330092121525)
  
  3、浏览器的缩放比例必须设置为100%
  
  4、IE11需要更改注册表
  
  32位
  
  ```
  HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\InternetExplorer\Main\FeatureControl\FEATURE_BFCACHE
  ```
  
  64位
  
  ```
  HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\InternetExplorer\Main\FeatureControl\FEATURE_BFCACHE
  ```
  
  若key值不存在，新建一个项FEATURE_BFCACHE 
  
  ![](https://img-blog.csdn.net/20160330094052876)

# 问题汇总

## sendkeys输入慢的问题

​	64为驱动sendkeys时很慢，使用32位驱动即可

