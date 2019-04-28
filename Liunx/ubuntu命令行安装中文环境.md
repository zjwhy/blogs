# ubuntu命令行安装中文环境

## 查看当前语言环境

```
echo $LANG
```

## 安装中文语言包

```
sudo apt update
sudo apt install language-pack-zh-hans
```

## 编辑 locale文件

```
sudo vim /etc/default/locale
```

```
LANG="zh_CN.UTF-8"
LANGUAGE="zh_CN:zh"
LC_NUMERIC="zh_CN"
LC_TIME="zh_CN"
LC_MONETARY="zh_CN"
LC_PAPER="zh_CN"
LC_NAME="zh_CN"
LC_ADDRESS="zh_CN"
LC_TELEPHONE="zh_CN"
LC_MEASUREMENT="zh_CN"
LC_IDENTIFICATION="zh_CN"
LC_ALL="zh_CN.UTF-8"
```



## 编辑   environment 文件

```
sudo vim /etc/environment
```

```
LANG="zh_CN.UTF-8"
LANGUAGE="zh_CN:zh"
LC_NUMERIC="zh_CN"
LC_TIME="zh_CN"
LC_MONETARY="zh_CN"
LC_PAPER="zh_CN"
LC_NAME="zh_CN"
LC_ADDRESS="zh_CN"
LC_TELEPHONE="zh_CN"
LC_MEASUREMENT="zh_CN"
LC_IDENTIFICATION="zh_CN"
LC_ALL="zh_CN.UTF-8"
```

# 重启 检查语言环境是否切换成功

```
sudo reboot
echo $LANG
```

