**官方DOC**

官网：https://build-system.fman.io/pyqt5-tutorial

整合资源 ：http://www.qter.org/portal.php?mod=list&catid=18



# 安装(windows)

```
pip install PyQt5==5.9.2
```

# setWindowFlags

Qt::Widget: QWidget构造函数的默认值，如果新的窗口部件没有父窗口部件，则它是一个独立的窗口，否则就是一个子窗口部件
Qt::Window: 无论是否有父窗口部件，新窗口部件都是一个窗口，通常有一个窗口边框和一个标题栏
Qt::Dialog: 新窗口部件是一个对话框，它是QDialog构造函数的默认值
Qt::Sheet： 新窗口部件是一个Macintosh表单(sheet)
Qt::Drawer: 新窗口部件是一个Macintosh抽屉(drawer)
Qt::Popup: 新窗口部件是一个弹出式顶层窗口
Qt::Tool: 新窗口部件是一个工具(tool)窗口，它通常是一个用于显示工具按钮的小窗口。如果一个工具窗口有父窗口部件，则它将显示在父窗口的部件上面，否则相当于使用了Qt::WindowStaysOnTopHint提示。
Qt::ToolTip: 新窗口部件是一个提示窗口，没有标题栏和窗口边框
Qt::Desktop: 新窗口部件是桌面，它是QDesktopWidget构造函数的默认值
Qt::SplashScreen: 新窗口部件是一个欢迎窗口，它是SplashScreen构造函数的默认值。
Qt::SubWindow: 新窗口部件是一个子窗口，而无论窗口部件是否有父窗口部件。此外，Qt还定义了一些控制窗口外观的窗口提示（这些窗口提示仅对顶层窗口有效）
Qt::MSWindowFiredSizeDialogHint: 为Windows系统上的窗口装饰一个窄的对话框边框，通常这个提示用于固定大小的对话框
Qt::MSWindowOwnDC: 为Windows系统上的窗口添加自身的显示上下文菜单
Qt::X11BypassWindowManagerHint: 完全忽视窗口管理器，它的作用是产生一个根本不被管理的无窗口边框的窗口(此时，用户无法使用键盘进行输入，除非手动调用QWidget::activateWindow()函数)
Qt::FramelessWindowHint: 产生一个无窗口边框的窗口，此时用户无法移动该窗口和改变它的大小
Qt::CustomizeWindowHint: 关闭默认的窗口标题提示
Qt::WindowTitleHint： 为窗口装饰一个标题栏
Qt::WindowSystemMenuHint: 为窗口添加一个窗口系统系统菜单，并尽可能地添加一个关闭按钮
Qt::WindowMinimizeButtonHint: 为窗口添加一个“最小化”按钮
Qt::WindowMaximizeButtonHint: 为窗口添加一个“最大化”按钮
Qt::WindowMinMaxButtonHint: 为窗口添加一个“最小化”按钮 和一个“最大化”按钮
Qt::WindowContextHelpButtonHint: 为窗口添加一个“上下文帮助”按钮
Qt::WindowStaysOnTopHint: 告知窗口系统，该窗口应该停留在所有其他窗口的上面。
Qt::WindowType_Mask: 一个用于提示窗口标识的窗口类型部分的掩码