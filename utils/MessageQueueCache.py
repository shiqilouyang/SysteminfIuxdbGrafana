from functools import lru_cache
from collections import deque

class MessageQueueCache():
    def __init__(self):
        self.q = deque()

    def put(self, data={}):
        self.q.appendleft(data)

    def get(self):
        try:
            data = self.q.pop()
        except IndexError:
            return
        return data

    @classmethod
    @lru_cache(None, typed=False)
    def useCache(cls, data):
        def cache(data):
            return data
        return cache(data)
