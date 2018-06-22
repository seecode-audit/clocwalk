# coding: utf-8


class CBaseException(Exception):
    pass


class ConnectionException(Exception):
    pass


class DataException(CBaseException):
    pass


class SyntaxException(CBaseException):
    pass


class GenericException(CBaseException):
    pass


class UserQuitException(CBaseException):
    pass
