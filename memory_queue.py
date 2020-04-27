import time
import redis


class RedisMem:
    db = 2
    password = 123456
    host = '10.168.1.245'
    port = 6379
    pool = redis.ConnectionPool(host=host, port=port, decode_responses=True, password=password, db=db)
    r = redis.Redis(connection_pool=pool)

    def __init__(self, level=''):
        self.level = level

    def set(self, key, val, ex=None, remove_exist=False):
        """
        remove  False旧的不会被删除
        ex      过期时间(秒)
        """
        key = self.level + key
        if remove_exist:
            self.r.delete(key)

        if type(val) == list:
            self.r.lpush(key, *val)  # [...,3,2,1]
        elif type(val) == dict:
            self.r.hmset(key, val)
        elif type(val) == set:
            self.r.sadd(key, *val)
        else:
            self.r.set(key, val)

        if ex:
            self.r.expire(key, ex)


class ExpSet(RedisMem):
    def __init__(self, key, level=''):
        super(ExpSet, self).__init__(level=level)
        self.key = self.level + key
        self.exp = None

    def set_item(self, elems: set):
        for item in elems:
            self.r.zadd(self.key, {item: time.time()})

    def flush(self, exp):
        self.r.zremrangebyscore(self.key, 0, time.time() - exp)


if __name__ == '__main__':
    # r = RedisMem()
    e = ExpSet(key='alice', level='fxh:')

