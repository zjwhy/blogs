'''
错误核心模块
'''


from enum import IntEnum, unique


@unique
class UIAErrorCode(IntEnum):
    ValidationFail = -2
    Unknown = -1
    Common = 1
    UIDriverConnectionError = 9
    CEFBrowserConnectionError = 10
    NMHConnectionError = 11
    NoChromeBridgeError = 12
    NonsupportOperation = 13
    MobileDeviceManagerConnectionError = 14
    NoJavaExtensionError = 15
    NoSuchWindow = 100
    NoSuchElement = 101
    NoSuchFrame = 102
    PageIsLoading = 103
    FrameIsLoading = 104
    JavaScriptError = 105
    NoSuchElementID = 106
    NoSuchImage = 107
    Timeout = 108
    AIError = 109
    DriverInputError = 111


class UIAError(Exception):
    """SDK异常基类
    """

    def __init__(self, message, code):
        """SDK异常基类

        `message`: 错误信息
        """
        super().__init__(message)
        self.code = code
