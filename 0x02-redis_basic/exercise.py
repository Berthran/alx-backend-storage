#!/usr/bin/env python3
'''
A redis class
'''


import redis
import uuid
from typing import Union


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

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        Takes a data and returns a string
        '''
        randKey: str = str(uuid.uuid4())
        self._redis.set(randKey, data)
        return randKey
