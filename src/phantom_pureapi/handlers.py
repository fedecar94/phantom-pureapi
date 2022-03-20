from typing import List, Tuple, AnyStr
from urllib.parse import parse_qs
from .loggers import get_custom_logger
from .mixins import HTMLResponseMixin, JSONResponseMixin, MsgPackResponseMixin
from .auth import AuthHandler
from .utils import get_content_type_from_headers
from msgpack import dumps, loads

logger = get_custom_logger(__name__)


class BaseHandler(HTMLResponseMixin, JSONResponseMixin, MsgPackResponseMixin):
    status_code = 200
    body = dict()
    headers = list()
    template_name = "default.html"
    _auth_handler = AuthHandler()

    async def handle_event(self, redis, scope, receive):
        headers = scope.get("headers", list())
        user = await self.authenticate(headers)
        content_type = get_content_type_from_headers(scope.get("headers"))
        method = scope.get('method', 'GET').lower()

        if method == 'get':
            path = scope.get('path')
            cached_response_key = f"{method}/{user.pk}/{content_type}/{path}"
            cached_response = await redis.get(cached_response_key)
            if cached_response is not None:
                return loads(cached_response)
            else:
                event = b""
        else:
            event = await receive()

        logger.debug("event: %s", event)

        query_string = parse_qs(scope.get("query_string"))
        logger.debug("query_string: %s", query_string)

        ####################
        # TODO handle here #
        ####################

        headers_func_name = f"headers_as_{content_type.split('/')[1]}"
        headers_func = self.__getattribute__(headers_func_name)

        body_func_name = f"body_as_{content_type.split('/')[1]}"
        body_func = self.__getattribute__(body_func_name)

        response_dict = {
            b"headers": headers_func(),
            b"body": body_func(),
            b"status_code": self.status_code
        }

        if method == 'get':
            await redis.set(cached_response_key, dumps(response_dict))
            await redis.pexpire(cached_response_key, 60 * 1000)

        return response_dict

    def authenticate(self, headers: List[Tuple[AnyStr, AnyStr]] = None):
        return self._auth_handler(headers or list())
