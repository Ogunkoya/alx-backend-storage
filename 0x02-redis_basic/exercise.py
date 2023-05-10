#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Callable
import ast
from functools import wraps

class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()
        self.call_counts = {}

    def count_calls(self, method: Callable) -> Callable:
        @wraps(method)
        def wrapper(*args, **kwargs):
            key = method.__qualname__
            self.call_counts[key] = self.call_counts.get(key, 0) + 1
            return method(*args, **kwargs)
        return wrapper

    def call_history(self, method: Callable) -> Callable:
        @wraps(method)
        def wrapper(*args, **kwargs):
            input_key = f"{method.__qualname__}:inputs"
            output_key = f"{method.__qualname__}:outputs"

            self._redis.rpush(input_key, str(args))
            output = method(*args, **kwargs)
            self._redis.rpush(output_key, str(output))

            return output
        return wrapper

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    

    def replay(self, method: Callable):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        input_list = self._redis.lrange(input_key, 0, -1)
        output_list = self._redis.lrange(output_key, 0, -1)

        call_history = []
        for inputs, output in zip(input_list, output_list):
            inputs = ast.literal_eval(inputs.decode())
            output = ast.literal_eval(output.decode())
            call_history.append((inputs, output))

        return call_history