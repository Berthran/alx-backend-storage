#!/usr/bin/env python3
'''
A redis class
'''


import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper_incr(self, *args, **kwargs):
        '''
        increments count for the key
        '''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper_incr


class Cache:
    '''
    A storage class with Redis
    '''

    def __init__(self) -> None:
        '''
        Constructor method
        '''
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        Takes a data and returns a string
        '''
        randKey: str = str(uuid.uuid4())
        if data is not None:
            self._redis.set(randKey, data)
            return randKey
        return randKey

    def get(self, key: str, fn=None):
        '''
        reads from Redis and recover original type
        '''
        redisData = self._redis.get(key)
        if redisData is None:
            return None
        if fn:
            data = fn(redisData)
            return data
        return redisData

    def get_str(self, key: str) -> Optional[str]:
        '''
        Gets a value from Redis and converts to a string
        '''
        return self.get(key, lambda value: value.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        '''
        Gets a value from Redis and converts to an int
        '''
        return self.get(key, lambda value: int(value))
