# coding: utf-8


class CodeBaseException(Exception):
    pass


class ConnectionException(Exception):
    pass


class DataException(CodeBaseException):
    pass


class SyntaxException(CodeBaseException):
    pass


class GenericException(CodeBaseException):
    pass


class UserQuitException(CodeBaseException):
    pass


class CodeDirIsNoneException(CodeBaseException):
    pass


class HTTPStatusCodeError(CodeBaseException):
    pass


class NoUpgradeRequiredError(CodeBaseException):
    pass

