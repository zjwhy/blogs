

class Cookies(object):
    # https://github.com/SeleniumHQ/selenium/wiki/JsonWireProtocol#cookie-json-object
    def __init__(self, controller):
        self._controller = controller

    def get(self, url=None, domain=None, name=None):
        pass

    def set(self, url, name, *, domain=None, value=None, path=None, secure=False, httpOnly=False, expirationDate=None):
        pass

    def remove(self, name):
        pass
