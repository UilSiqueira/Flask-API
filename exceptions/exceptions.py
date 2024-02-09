from werkzeug.exceptions import HTTPException


class NotFoundValue(HTTPException):
    code = 400


class QuantityException(HTTPException):
    code = 400
