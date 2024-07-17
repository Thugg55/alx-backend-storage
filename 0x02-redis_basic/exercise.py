#!/usr/bin/env python3
"""
create a cache class
store an instance of redis-cli
define the count_calls decorator
use the INCR command
define the call_history decorator
use the RPUSH, LPUSH and LRANGE commands
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

def call_history(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))

        result = method(self, *args, **kwargs)

        self._redis.rpush(output_key, str(result))

        return result

    return wrapper

def replay(method: Callable) -> None:
    redis_client = redis.Redis()
    method_name = method.__qualname__

    calls = int(redis_client.get(f"{method_name}:calls") or 0)
    inputs = redis_client.lrange(f"{method_name}:inputs", 0, -1)
    outputs = redis_client.lrange(f"{method_name}:outputs", 0, -1)

    print(f"{method_name} was called {calls} times:")
    for inp, outp in zip(inputs, outputs):
        print(f"{method_name}(*{inp.decode('utf-8')}) -> {outp.decode('utf-8')}")

class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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

# Usage example:
# cache = Cache()
# cache.store("foo")
# cache.store("bar")
# cache.store(42)
# replay(cache.store)
