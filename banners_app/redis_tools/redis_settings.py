from . import *


class MyRedis:
    rd: redis = None

    @classmethod
    def connect_redis(cls):
        cls.rd = redis.Redis(host=settings.REDIS_HOST,
                             port=settings.REDIS_PORT, db=0)
