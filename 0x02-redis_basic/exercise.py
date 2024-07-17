#!/usr/bin/env python3
"""
create a cache class
store an instance of redis-cli
"""

import redis
import uuid
from typing import Union

class Cache:
    
    
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key



    def get (self,key: str, fn: optional[callable[[bytes]
        union[str, int, float]]] = None -> union[str, int, float, None]:
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data


    def get_str(self, key:str) -> union[str, None]:
        return self.get(key, lambda data: data.decode('utf-8'))


    def get_int(self, key:str) -> union[int, None]:
        return self.get(key, int)
