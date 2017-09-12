from time import sleep
from redis.client import Redis

redis = Redis(host='localhost', port=6379, db=0, password=None)


class Lock:
    def __enter__(self):
        self.lock = redis.lock('tyr.lock|' + self.instance, timeout=60*120)
        print "on entre dans le lock"
        if not self.lock.acquire(blocking=False):
            print "ca merde..."
            raise "ayamas marche"

    def __exit__(self, exc_type, exc_value, traceback):
        print 'Cleaning up MyResource'
        self.lock.release()

    def __init__(self, instance):
        print 'Constructing MyResource'
        self.instance = instance


def job():
    with Lock('bob'):
        sleep(10000)


job()