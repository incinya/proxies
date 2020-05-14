from memory.redis_memory import RedisExpSet


class ProxyStack:
    key = 'prox:stack'
    mem_set = RedisExpSet(key)

    @staticmethod
    def en_stack(url):
        ProxyStack.mem_set.set(url)

    @staticmethod
    def de_stack():
        return ProxyStack.mem_set.get_newest()

    @staticmethod
    def get_size():
        return ProxyStack.mem_set.get_size()
