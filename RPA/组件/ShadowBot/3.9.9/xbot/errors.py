'''
错误核心模块
'''


from enum import IntEnum, unique


@unique
class UIAErrorCode(IntEnum):
    ValidationFail = -2 # 参数验证失败
    Unknown = -1 # 未知异常
    Common = 1 # 通用异常
    UnHandle = 0 # 未处理异常
    UIDriverConnectionError = 9 # UIDriver连接错误
    CEFBrowserConnectionError = 10 # 内置浏览器连接异常
    ChromeBridgeConnectionError = 11 # ChromeBridge进程连接错误
    NoChromeBridgeError = 12 # 尚未安装Chrome插件
    NonsupportOperation = 13 # 元素不支持此自动化操作
    MobileDeviceManagerConnectionError = 14 # 无法连接到手机管理器
    NoJavaExtensionError = 15 # 尚未安装Java插件
    JsDialogOpened = 16 # 浏览器中存在弹框
    NoSuchWindow = 100 # 未找到窗口
    NoSuchElement = 101 # 未找到元素
    NoSuchFrame = 102 # 未找到域
    PageIsLoading = 103 # 网页尚未加载完成
    FrameIsLoading = 104 # 网页中的Frame尚未加载完成
    JavaScriptError = 105 # JavaScript执行出错
    NoSuchElementID = 106 # 未找到元素指定的元素ID（缓存失效）
    NoSuchImage = 107 # 未找到图像
    Timeout = 108 # 操作超时
    AIError = 109 # AI识别错误
    DriverInputError = 110 # 无法通过驱动模拟按键输入
    CDPMethodNotFound = 111 # 未找到CDP的方法


class UIAError(Exception):
    """SDK异常基类
    """

    def __init__(self, message, code):
        """SDK异常基类

        `message`: 错误信息
        """
        super().__init__(message)
        self.code = code
