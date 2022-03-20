from pathlib import Path

import pureapi.exceptions
from ujson import dumps as json_dumps
from msgpack import dumps as msgpack_dumps
from mako.template import Template
from .loggers import get_custom_logger

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

logger = get_custom_logger(__name__)
__all__ = ['HTMLResponseMixin', 'JSONResponseMixin', 'MsgPackResponseMixin']


class HTMLResponseMixin:
    template_name = None
    body = dict()
    headers = list()

    def _get_template_name(self):
        if not self.template_name:
            raise NotImplementedError('Please define a template name first')

        template_name = BASE_DIR / "pureapi" / "templates" / self.template_name
        logger.debug("template_name: %s", template_name)
        return str(template_name)

    def _get_template_args(self, **kwargs):
        kwargs.update(**self.body)
        if "title" not in kwargs:
            kwargs["title"] = "Default response"
        kwargs["json"] = json_dumps(self.body)
        return kwargs

    def headers_as_html(self):
        return self.headers + [
            [b"content-type", b"text/html"],
        ]

    def body_as_html(self):
        try:
            response = Template(
                filename=self._get_template_name(), module_directory="/tmp/mako_modules"
            )
            return response.render(**self._get_template_args()).encode(encoding="UTF-8")
        except Exception as e:
            logger.error('%s', e)
            raise pureapi.exceptions.HttpException()


class JSONResponseMixin:
    body = dict()
    headers = list()

    def headers_as_json(self):
        return self.headers + [
            [b"content-type", b"application/json"],
        ]

    def body_as_json(self):
        try:
            return json_dumps(self.body).encode(encoding="UTF-8")
        except Exception as e:
            logger.error('%s', e)
            raise pureapi.exceptions.HttpException()


class MsgPackResponseMixin:
    body = dict()
    headers = list()

    def headers_as_msgpack(self):
        return self.headers + [
            [b"content-type", b"application/msgpack"],
        ]

    def body_as_msgpack(self):
        try:
            return msgpack_dumps(self.body)
        except Exception as e:
            logger.error('%s', e)
            raise pureapi.exceptions.HttpException()
