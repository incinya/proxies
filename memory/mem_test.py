import time
from unittest import TestCase

from logger import logger
from memory.memory_queue import ExpSet, RedisMem

log = logger()


class MemTst(TestCase):
    def setUp(self) -> None:
        ...

    def test_mock_zset(self):
        e = ExpSet(set_name='alice', level='fxh:')
        for i in range(1000, 0, -1):
            e.set_items({str(i)})
            log.debug('setItem'+str(i))
            time.sleep(0.5)

    def test_set_item(self):
        r = RedisMem()
        r.set('alice', {'d': 'MyHonor', 'e': 'LordAlice', 'f': 'myLord'}, ex=10)

    def test_flush(self):
        e = ExpSet(set_name='alice', level='fxh:')
        e.flush(20)
