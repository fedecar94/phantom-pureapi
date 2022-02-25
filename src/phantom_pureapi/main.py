from pathlib import Path
from typing import Type, List, Dict, Union
from urllib.parse import parse_qs

from phantom_pureapi import exceptions, utils
from .handlers import BaseHandler
from .loggers import logger
from .urls import list_to_dict, UrlPath, SubPath

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class PureApi:
    _urlpatterns: Dict = dict

    def __init__(self) -> None:
        # TODO: init redis and psql here
        pass

    async def __call__(self, scope, receive, send):
        logger.warning('-> Incomming request!')
        logger.debug(scope)

        headers = scope.get('headers')
        logger.debug(headers)
        accept_list, language_list = utils.parse_headers(headers)

        query_string = parse_qs(scope.get('query_string'))
        logger.debug(query_string)

        event = await receive()
        logger.debug(event)

        try:
            handler = self._get_handler(scope['path'])
            logger.debug(handler)
            response = handler()
        except exceptions.HttpException as ex:
            await send({
                'type': 'http.response.start',
                'status': ex.status_code,
                'headers': [
                    [b'content-type', b'aplication/json'],
                ]
            })
            await send({
                'type': 'http.response.body',
                'body': ex.as_json(),
            })
        else:
            if b'text/html' in accept_list:
                await send({
                    'type': 'http.response.start',
                    'status': 200,
                    'headers': response.headers_as_html()
                })
                await send({
                    'type': 'http.response.body',
                    'body': response.as_html(),
                })
                return
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': response.headers_as_json()
            })
            await send({
                'type': 'http.response.body',
                'body': response.as_json(),
            })

    def _get_handler(self, request_path: str) -> Type[BaseHandler]:
        logger.debug(request_path)
        if request_path in self._urlpatterns:
            return self._urlpatterns[request_path]
        else:
            raise exceptions.HTTP404

    @property
    def urlpatterns(self) -> Dict:
        return self._urlpatterns

    @urlpatterns.setter
    def urlpatterns(self, urls: List[Union[UrlPath, SubPath]]) -> None:
        self._urlpatterns = list_to_dict(urls)
