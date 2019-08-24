# 安装

# 汉化

1、ctrl+shift+P 组合键 启动命令模式

2、搜索 

```
Configure display language
```

3、install add language packs

4、选择中文语言包安装，右下角提示用户更新语言，选择确定重启vscode

# 报错处理

```
Unable to install extension 'ms-ceintl.vscode-language-pack-zh-hans' as it is not compatible with VS Code '1.37.1'.
```

更换语言包版本版本就好了

```
Unable to install extension 'ms-ceintl.vscode-language-pack-zh-hans' as it is not compatible with VS Code '1.37.1'.
```

 该情况是extension没有权限，更改目录权限就好 [原博主链接](https://blog.csdn.net/doushanyou9100/article/details/84630192)

```
sudo chown -R 你的用户名 ~/.vscode/extensions
```

