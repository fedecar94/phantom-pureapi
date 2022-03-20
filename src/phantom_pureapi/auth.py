from abc import ABC
from typing import List, AnyStr
from .utils import get_auth_token_from_headers
from .loggers import get_custom_logger

logger = get_custom_logger(__name__)


class AbstractUser(ABC):
    _pk = None
    _authenticated = True
    _scopes = []
    extras = dict()

    def __init__(self, pk=None, scopes: List[AnyStr] = None, **kwargs):
        self._pk = pk
        self._scopes = scopes or list()
        self.extras = kwargs

    @property
    def pk(self):
        return self._pk

    @property
    def authenticated(self):
        return self._authenticated

    @property
    def scopes(self):
        return self._scopes


class AnonymousUser(AbstractUser):
    authenticated = False


class AuthHandler:
    async def __call__(self, headers: List):
        if token := get_auth_token_from_headers(headers or list()):
            logger.debug(token)
        return AnonymousUser
