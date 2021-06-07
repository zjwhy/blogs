# ADCRPARobot

#一. ADCRPARobot项目Python环境构建详情

**1.如本地开发，则只需安装requirements.txt文件中注明的依赖库：**

pip install -r requirements.txt

# 二. ADCRPARobot项目Linux环境适配

**1.配置java环境**

下载安装jdk
设置环境变量，修改/etc/profile文件，在文件末尾添加,(如jdk地址为：/home/jdk1.5.0)
export JAVA_HOME=/home/jdk1.5.0
export PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar

**2.配置chromium-driver环境**

使用终端安装chromium-driver, 命令：apt-get install chromium-driver

**3. 启动robot运行脚本**
进入robot安装路径下的Robot文件夹下
设置weAutomate为可执行文件：chmod a+x weAutomate
运行脚本：./weAutomate -w case路径