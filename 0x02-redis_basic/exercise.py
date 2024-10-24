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
    def wrapper_incr(self, *args, **kwargs) -> Any:
        '''
        increments count for the key
        '''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper_incr


def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
        store history of inputs and outputs for a particular function
        '''
        key_inputs = f"{method.__qualname__}:inputs"
        key_outputs = f"{method.__qualname__}:outputs"
        self._redis.rpush(key_inputs, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(key_outputs, output)
        return output
    return wrapper


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
    @call_history
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


def replay(func: Callable) -> None:
    '''
    Display the history of calls for a given method
    '''
    r = redis.Redis()
    func_name = func.__qualname__  # Get the function's qualified name
    key_inputs = f"{func_name}:inputs"
    key_outputs = f"{func_name}:outputs"

    # Fetch inputs and outputs from Redis
    inputs = r.lrange(key_inputs, 0, -1)  # Fetch all input entries
    outputs = r.lrange(key_outputs, 0, -1)  # Fetch all output entries

    # Display the call history
    print(f"{func_name} was called {len(inputs)} times:")

    # Use zip to pair inputs and outputs
    for input_data, output_data in zip(inputs, outputs):
        print(f"{func_name}(*{input_data.decode('utf-8')}) -> \
                {output_data.decode('utf-8')}")
