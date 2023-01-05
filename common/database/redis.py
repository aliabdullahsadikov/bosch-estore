"""
Instruction of redis usage

# library
pip install redis

# full documentation
https://realpython.com/python-redis/

"""
import datetime

import redis
import pickle

redis_client = redis.Redis(
    host="127.0.0.1",
    port=6379,
    db=0,
    password=None
)


def cache_up(func):
    """
    Decorator for caching
    """
    def wrapp(*args, **kwargs):
        if redis_client.exists("categories"):
            print("from cache")
            categories_in_bytes = redis_client.get("categories")
            categories = pickle.loads(categories_in_bytes)

        else:
            categories = func()
            if categories:
                pickled = pickle.dumps(categories)
                redis_client.set("categories", value=pickled)
                redis_client.expire("categories", datetime.timedelta(minutes=20))

                print("from db")

        return categories

    return wrapp

