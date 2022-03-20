from .loggers import get_custom_logger

from pureapi import exceptions
from collections import namedtuple
from typing import List, Dict, Union

logger = get_custom_logger(__name__)

UrlPath = namedtuple("UrlPath", "path handler")
SubPath = namedtuple("SubPath", "prefix patterns")


def _get_urls(prefix: str, urls: List[Union[UrlPath, SubPath]]) -> List[UrlPath]:
    patterns = list()
    for url in urls:
        if isinstance(url, UrlPath):
            patterns.append(UrlPath(prefix + url.path, url.handler))
        elif isinstance(url, SubPath):
            for _url in _get_urls(url.prefix, url.patterns):
                patterns.append(UrlPath(prefix + _url.path, url.handler))
        else:
            raise exceptions.PathTypeException
    return patterns


def list_to_dict(urls: List[Union[UrlPath, SubPath]]) -> Dict:
    patterns = dict()
    for url in urls:
        if isinstance(url, UrlPath):
            if not (url.path.startswith("/") and url.path.endswith("/")):
                raise exceptions.PathException
            patterns[url.path] = url.handler
        elif isinstance(url, SubPath):
            for _url in _get_urls(url.prefix, url.patterns):
                if not (_url.path.startswith("/") and _url.path.endswith("/")):
                    raise exceptions.PathException
                patterns[_url.path] = _url.handler
        else:
            raise exceptions.PathTypeException
    return patterns
