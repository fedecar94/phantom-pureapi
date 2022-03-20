from typing import AnyStr

import pureapi.mixins


class PathException(Exception):
    message = 'Your paths should start and end with "/"'

    def __str__(self):
        return self.message


class PathTypeException(Exception):
    message = "Your path is not the correct type"

    def __str__(self):
        return self.message


class HttpException(Exception, pureapi.mixins.HTMLResponseMixin, pureapi.mixins.JSONResponseMixin):
    title = "Unexpected Error"
    message = "¯\\_(ツ)_/¯"
    status_code = 500
    error_code = 500
    template_name = "error.html"

    def __init__(self):
        self.body = {
            "title": self.title,
            "message": self.message,
            "error_code": self.error_code,
        }

    def get_headers(self, content_type: AnyStr = b"application/json"):
        if content_type == b"text/html":
            return self.headers_as_html()
        return self.headers_as_json()

    def get_body(self, content_type: AnyStr = b"application/json"):
        if content_type == b"text/html":
            return self.body_as_html()
        return self.body_as_json()


class HTTP401(HttpException):
    title = "Unauthorized"
    message = "the request lacks valid authentication credentials"
    status_code = 401
    error_code = 401


class HTTP404(HttpException):
    title = "Not found"
    message = "the resource you are looking for may not exist"
    status_code = 404
    error_code = 404
