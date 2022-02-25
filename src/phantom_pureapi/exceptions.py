
from ujson import dumps


class PathException(Exception):
    message = 'Your paths should start and end with "/"'

    def __str__(self):
        return self.message


class PathTypeException(Exception):
    message = 'Your path is not the correct type'

    def __str__(self):
        return self.message


class HttpException(Exception):
    title = 'Unexpected Error'
    message = '¯\\_(ツ)_/¯'
    status_code = 500
    error_code = 500

    def as_json(self):
        response = {
            'title': self.title,
            'message': self.message,
            'error_code': self.error_code,
        }
        return dumps(response).encode(encoding='UTF-8')


class HTTP404(HttpException):
    title = 'Not found'
    message = 'the resource you are looking for may not exist'
    status_code = 404
    error_code = 404
