from . import *


class MyRedis:
    rd: redis = None

    @classmethod
    def connect_redis(cls):
        cls.rd = redis.Redis(host="localhost", port=6379, db=0)
