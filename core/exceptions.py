from rest_framework.exceptions import APIException
from rest_framework import status

class PythonTipError(Exception):
    """
    A generic exception for all others to extend.
    """
    pass


class MissingAuthKey(PythonTipError):
    pass


class InvalidAuthKey(PythonTipError):
    pass


class GoogleFormError(APIException):
    pass


class SimilarEntryException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
