import redis

r = redis.Redis(host="redis", port=6379, decode_responses=True)


def get_redis():
    return r


def connect_redis():
    try:
        r.ping()
        return r
    except redis.ConnectionError as e:
        return None