from pathlib import Path

import ujson
from mako.template import Template
from ujson import dumps

from pureapi.exceptions import HttpException
from pureapi.loggers import logger

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class BaseHandler:
    status_code = 200
    body = dict()
    headers = list()
    template_name = 'default.html'

    def headers_as_html(self):
        return self.headers + [
            [b'content-type', b'text/html'],
        ]

    def _get_template_name(self):
        template_name = BASE_DIR / 'phantom_pureapi' / 'templates' / self.template_name
        logger.debug(template_name)
        return str(template_name)

    def _get_template_args(self, **kwargs):
        kwargs.update(**self.body)
        if 'title' not in kwargs:
            kwargs['title'] = 'Default response'
        kwargs['json'] = ujson.dumps(self.body)
        kwargs['body'] = self.body
        return kwargs

    def as_html(self):
        try:
            response = Template(filename=self._get_template_name(),
                                module_directory='/tmp/mako_modules')
            return response.render(**self._get_template_args()).encode(encoding='UTF-8')
        except Exception as e:
            logger.error(e)
            raise HttpException()

    def headers_as_json(self):
        return self.headers + [
            [b'content-type', b'aplication/json'],
        ]

    def as_json(self):
        try:
            return dumps(self.body).encode(encoding='UTF-8')
        except Exception as e:
            logger.error(e)
            raise HttpException()


