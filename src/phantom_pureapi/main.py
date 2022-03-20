from pathlib import Path
import aioredis
from typing import Type, List, Dict, Union

from pureapi import exceptions, utils
from .handlers import BaseHandler
from .urls import list_to_dict, UrlPath, SubPath
from .loggers import get_custom_logger

logger = get_custom_logger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class PureApi:
    _urlpatterns: Dict = dict

    def __init__(self) -> None:
        # TODO: init redis and psql here
        self.redis = aioredis.from_url("redis://localhost")

    async def __call__(self, scope, receive, send):
        logger.info("Incomming request!")
        logger.debug("scope: %s", scope)

        try:
            handler = self._get_handler(scope["path"])
            logger.debug("handler: %s", handler)
            response = await handler.handle_event(redis=self.redis, scope=scope, receive=receive)
            await send({
                "type": "http.response.start",
                "status": response[b'status_code'],
                "headers": response[b'headers'],
            })
            await send({
                "type": "http.response.body",
                "body": response[b'body'],
            })
        except exceptions.HttpException as ex:
            content_type = utils.get_content_type_from_headers(scope.get("headers"))
            await send({
                "type": "http.response.start",
                "status": ex.status_code,
                "headers": ex.get_headers(content_type),
            })
            await send({
                "type": "http.response.body",
                "body": ex.get_body(content_type),
            })

    def _get_handler(self, request_path: str) -> Type[BaseHandler]:
        logger.debug(request_path)
        if request_path in self._urlpatterns:
            handler = self._urlpatterns[request_path]
            return handler()
        else:
            raise exceptions.HTTP404

    @property
    def urlpatterns(self) -> Dict:
        return self._urlpatterns

    @urlpatterns.setter
    def urlpatterns(self, urls: List[Union[UrlPath, SubPath]]) -> None:
        self._urlpatterns = list_to_dict(urls)
