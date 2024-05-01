import redis
import json
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

REDIS_SERVER = os.getenv('REDIS_SERVER', 'localhost')
cache = redis.Redis(REDIS_SERVER)


def setData(request_id, request_data):
    value = json.dumps(request_data)
    cache.set(request_id, value)
    cache.expire(request_id, 60*60*8)


def getData(request_id):
    value = cache.get(request_id)
    if value is not None:
        return json.loads(value)
    return None


def deleteData(request_id):
    cache.delete(request_id)


def flushAll():
    cache.flushall()
