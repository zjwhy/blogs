# 下载tar包

[官方下载压缩包](https://www.getpostman.com/downloads/)

# 安装

1、 进入下载目录解压

```
sudo  tar -xzf postman.tar.gz	-C /opt/
```

2、 执行Postman安装

```
/Postman/Postman
```

3、创建全局变量

```
sudo ln -s /opt/Postman/Postman /usr/bin/postman
```

4、添加启动器应用图标

```
sudo vim /usr/share/applications/postman.desktop
```

添加内容

```
[Desktop Entry]

Encoding=UTF-8

Name=Postman

Exec=postman

Icon=/opt/Postman/app/resources/app/assets/icon.png

Terminal=false

Type=Application

Categories=Development;
```