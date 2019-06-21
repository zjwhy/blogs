# 安装Visio报错 提示已经安装32位与64位冲突	

![](https://imgsa.baidu.com/exp/w=500/sign=11b3606c0a082838680ddc148898a964/9922720e0cf3d7ca4d07f405ff1fbe096a63a9d4.jpg)



# 解决办法，修改注册表

组合键	win + R  输入regedit运行注册表

找到 HKEY_CLASSES_ROOT\Installer\Products\ 下值为 提示冲突的那一项，删除该项，指向安装。![](https://imgsa.baidu.com/exp/w=500/sign=50a7956fd90735fa91f04eb9ae500f9f/a8773912b31bb05103a6845c3b7adab44bede0c0.jpg)

