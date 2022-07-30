import requests


class CatsOfflineException(BaseException):
    pass


class CatsAnswerCodeException(BaseException):
    def __init__(self, response: requests.Response):
        self.response = response


class CatsAuthorizationException(BaseException):
    pass


class CatsNormalErrorException(BaseException):
    def __init__(self, response: requests.Response):
        self.response = response
