## 采用MinGW的安装方式

1. 下载MinGW	[MinGW官网](http://www.mingw.org/)****

2. **管理员权限**启动安装程序， 选择

    ```
    mingw32-base-bin
    mingw32-gcc-g++-bin
    ```

    3.添加系统环境变量

    将安装目录下的bin添加到环境变量， （D:\MinGW\bin）

    4.检测 cmd 输入 gcc -v  和 g++ -v 输出版本号以及其它信息表示安装成功。