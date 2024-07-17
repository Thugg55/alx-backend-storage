#!/usr/bin/env python3
"""
create a cache class
store an instance of redis-cli
define the count_calls decorator
use the INCR command
"""

import redis
import uuid
from typing import Union, Callable, Optional
import functools

def count_calls(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = f"{method.__qualname__}:calls"
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[[bytes], Union[str, int, float]]] = None) -> Union[str, bytes, int, float, None]:
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, lambda data: data.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, int)
