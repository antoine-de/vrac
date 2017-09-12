__author__ = 'antoine'

from multiprocessing.dummy import Pool as ThreadPool


class Parallele:
    def __init__(self, nb_thread):
        self.pool = ThreadPool(nb_thread)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("leaving parallele for")
        self.pool.close()
        self.pool.join()

    def map(self, func, param):
        self.pool.map(func, param)


def long_function(i):
    print "starting ", i
    import time
    time.sleep(i)
    print "exiting ", i

print "c'est partiiii"
with Parallele(3) as p:
    p.map(long_function, [1, 4, 6, 15, 19])


print "fini"
